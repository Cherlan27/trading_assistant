<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import {
  createChart,
  CandlestickSeries,
  HistogramSeries,
  LineSeries,
} from 'lightweight-charts'
import type { IChartApi, ISeriesApi, Time, MouseEventParams } from 'lightweight-charts'
import type { OHLCVDataPoint, IndicatorData, IndicatorDataPoint, BollingerDataPoint } from '@/composables/useApi'
import { OVERLAY_COLORS, INDICATOR_COLORS, toTime } from '@/constants'

const props = defineProps<{
  primarySymbol: string
  primaryData: OHLCVDataPoint[] | null
  overlaySymbols: { symbol: string; data: OHLCVDataPoint[] }[]
  indicators: Record<string, IndicatorData>
  activeIndicators: string[]
}>()

const emit = defineEmits<{
  'crosshair-move': [data: any]
  'visible-range-change': [range: any]
}>()

const chartContainer = ref<HTMLDivElement>()
let chart: IChartApi | null = null
let candleSeries: ISeriesApi<'Candlestick'> | null = null
let volumeSeries: ISeriesApi<'Histogram'> | null = null
const overlaySeriesMap = new Map<string, ISeriesApi<'Line'>>()
const indicatorSeriesMap = new Map<string, ISeriesApi<'Line'>>()
let resizeObserver: ResizeObserver | null = null

function initChart() {
  if (!chartContainer.value) return

  chart = createChart(chartContainer.value, {
    layout: {
      background: { color: '#1a1a2e' },
      textColor: '#e0e0e0',
    },
    grid: {
      vertLines: { color: '#2B2B43' },
      horzLines: { color: '#2B2B43' },
    },
    crosshair: { mode: 0 },
    rightPriceScale: { borderColor: '#2B2B43' },
    timeScale: { borderColor: '#2B2B43' },
  })

  candleSeries = chart.addSeries(CandlestickSeries, {
    upColor: '#26a69a',
    downColor: '#ef5350',
    borderVisible: false,
    wickUpColor: '#26a69a',
    wickDownColor: '#ef5350',
  })

  volumeSeries = chart.addSeries(HistogramSeries, {
    priceScaleId: 'volume',
    priceFormat: { type: 'volume' },
  })
  chart.priceScale('volume').applyOptions({
    scaleMargins: { top: 0.8, bottom: 0 },
  })

  chart.subscribeCrosshairMove((param: MouseEventParams) => {
    if (!param.time || !param.seriesData) {
      emit('crosshair-move', null)
      return
    }

    const candleData = candleSeries ? param.seriesData.get(candleSeries) : null
    const volData = volumeSeries ? param.seriesData.get(volumeSeries) : null

    const indicatorValues: Record<string, number> = {}
    for (const [key, series] of indicatorSeriesMap) {
      const val = param.seriesData.get(series)
      if (val && 'value' in val) indicatorValues[key] = (val as any).value
    }
    for (const [sym, series] of overlaySeriesMap) {
      const val = param.seriesData.get(series)
      if (val && 'value' in val) indicatorValues[`overlay:${sym}`] = (val as any).value
    }

    emit('crosshair-move', {
      time: param.time,
      ohlcv: candleData && 'open' in candleData ? {
        open: (candleData as any).open,
        high: (candleData as any).high,
        low: (candleData as any).low,
        close: (candleData as any).close,
        volume: volData && 'value' in volData ? (volData as any).value : 0,
      } : undefined,
      indicatorValues,
    })
  })

  chart.timeScale().subscribeVisibleTimeRangeChange((range) => {
    emit('visible-range-change', range)
  })

  resizeObserver = new ResizeObserver(entries => {
    if (chart && entries[0]) {
      const { width, height } = entries[0].contentRect
      chart.resize(width, height)
    }
  })
  resizeObserver.observe(chartContainer.value)
}

function updatePrimaryData() {
  if (!candleSeries || !volumeSeries || !props.primaryData) return

  candleSeries.setData(props.primaryData.map(d => ({
    time: toTime(d.date),
    open: d.open,
    high: d.high,
    low: d.low,
    close: d.close,
  })))

  volumeSeries.setData(props.primaryData.map(d => ({
    time: toTime(d.date),
    value: d.volume,
    color: d.close >= d.open ? 'rgba(38, 166, 154, 0.5)' : 'rgba(239, 83, 80, 0.5)',
  })))
}

function updateOverlays() {
  if (!chart) return

  const currentSymbols = new Set(props.overlaySymbols.map(s => s.symbol))
  for (const [sym, series] of overlaySeriesMap) {
    if (!currentSymbols.has(sym)) {
      chart.removeSeries(series)
      overlaySeriesMap.delete(sym)
    }
  }

  props.overlaySymbols.forEach((overlay, idx) => {
    let series = overlaySeriesMap.get(overlay.symbol)
    if (!series) {
      series = chart!.addSeries(LineSeries, {
        color: OVERLAY_COLORS[idx % OVERLAY_COLORS.length],
        lineWidth: 2,
        priceScaleId: 'overlay',
      })
      overlaySeriesMap.set(overlay.symbol, series)
    }

    if (overlay.data.length === 0) return
    const base = overlay.data[0].close
    series.setData(overlay.data.map(d => ({
      time: toTime(d.date),
      value: ((d.close - base) / base) * 100,
    })))
  })

  if (props.overlaySymbols.length > 0 && chart) {
    chart.priceScale('overlay').applyOptions({
      scaleMargins: { top: 0.1, bottom: 0.2 },
    })
  }
}

function updateIndicators() {
  if (!chart) return

  const neededSeries = new Set<string>()
  for (const ind of props.activeIndicators) {
    if (ind === 'bbands_20') {
      neededSeries.add('bbands_20_upper')
      neededSeries.add('bbands_20_middle')
      neededSeries.add('bbands_20_lower')
    } else if (ind === 'rsi_14' || ind === 'macd') {
      continue
    } else {
      neededSeries.add(ind)
    }
  }

  for (const [key, series] of indicatorSeriesMap) {
    if (!neededSeries.has(key)) {
      chart.removeSeries(series)
      indicatorSeriesMap.delete(key)
    }
  }

  for (const key of neededSeries) {
    let series = indicatorSeriesMap.get(key)
    if (!series) {
      series = chart.addSeries(LineSeries, {
        color: INDICATOR_COLORS[key] || '#ffffff',
        lineWidth: key.startsWith('bbands_20') ? 1 : 2,
        priceScaleId: 'right',
      })
      indicatorSeriesMap.set(key, series)
    }

    const indKey = key.startsWith('bbands_20') ? 'bbands_20' : key
    const data = props.indicators[indKey]
    if (!data || data.length === 0) continue

    if (key.startsWith('bbands_20') && 'upper' in data[0]) {
      const bbandsData = data as BollingerDataPoint[]
      const field = key === 'bbands_20_upper' ? 'upper'
        : key === 'bbands_20_middle' ? 'middle' : 'lower'
      series.setData(bbandsData.map(d => ({
        time: toTime(d.date),
        value: d[field],
      })))
    } else if ('value' in data[0]) {
      const indData = data as IndicatorDataPoint[]
      series.setData(indData.map(d => ({
        time: toTime(d.date),
        value: d.value,
      })))
    }
  }
}

onMounted(() => {
  initChart()
  if (props.primaryData) {
    updatePrimaryData()
    updateOverlays()
    updateIndicators()
    chart?.timeScale().fitContent()
  }
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  chart?.remove()
  chart = null
})

watch(() => props.primaryData, () => {
  updatePrimaryData()
  chart?.timeScale().fitContent()
})

watch(() => props.overlaySymbols, updateOverlays, { deep: true })
watch(() => [props.indicators, props.activeIndicators], updateIndicators, { deep: true })
</script>

<template>
  <div ref="chartContainer" class="price-chart"></div>
</template>

<style scoped>
.price-chart {
  flex: 1;
  min-height: 400px;
}
</style>
