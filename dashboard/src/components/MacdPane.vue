<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { createChart, LineSeries, HistogramSeries } from 'lightweight-charts'
import type { IChartApi, ISeriesApi, Time } from 'lightweight-charts'
import type { MACDDataPoint } from '@/composables/useApi'

const props = defineProps<{
  data: MACDDataPoint[] | null
  visibleRange: { from: Time; to: Time } | null
}>()

const container = ref<HTMLDivElement>()
let chart: IChartApi | null = null
let macdLineSeries: ISeriesApi<'Line'> | null = null
let signalSeries: ISeriesApi<'Line'> | null = null
let histogramSeries: ISeriesApi<'Histogram'> | null = null
let resizeObserver: ResizeObserver | null = null
let syncing = false

onMounted(() => {
  if (!container.value) return

  chart = createChart(container.value, {
    layout: { background: { color: '#1a1a2e' }, textColor: '#e0e0e0' },
    grid: { vertLines: { color: '#2B2B43' }, horzLines: { color: '#2B2B43' } },
    rightPriceScale: {
      borderColor: '#2B2B43',
      scaleMargins: { top: 0.05, bottom: 0.05 },
    },
    timeScale: { borderColor: '#2B2B43', visible: false },
    height: 150,
  })

  histogramSeries = chart.addSeries(HistogramSeries, {
    priceFormat: { type: 'price', precision: 4, minMove: 0.0001 },
  })

  macdLineSeries = chart.addSeries(LineSeries, {
    color: '#2962FF',
    lineWidth: 1,
  })

  signalSeries = chart.addSeries(LineSeries, {
    color: '#FF6D00',
    lineWidth: 1,
  })

  resizeObserver = new ResizeObserver(entries => {
    if (chart && entries[0]) {
      chart.resize(entries[0].contentRect.width, 150)
    }
  })
  resizeObserver.observe(container.value)

  if (props.data) updateData()
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  chart?.remove()
  chart = null
})

function updateData() {
  if (!macdLineSeries || !signalSeries || !histogramSeries || !props.data) return

  const toT = (d: string) => d.slice(0, 10) as unknown as Time

  macdLineSeries.setData(props.data.map(d => ({
    time: toT(d.date),
    value: d.macd,
  })))

  signalSeries.setData(props.data.map(d => ({
    time: toT(d.date),
    value: d.signal,
  })))

  histogramSeries.setData(props.data.map(d => ({
    time: toT(d.date),
    value: d.histogram,
    color: d.histogram >= 0 ? 'rgba(38, 166, 154, 0.7)' : 'rgba(239, 83, 80, 0.7)',
  })))

  chart?.timeScale().fitContent()
}

watch(() => props.data, updateData)

watch(() => props.visibleRange, (range) => {
  if (range && chart && !syncing) {
    syncing = true
    try { chart.timeScale().setVisibleRange(range) } catch { /* range may not be valid */ }
    syncing = false
  }
})
</script>

<template>
  <div class="macd-pane">
    <div class="pane-label">MACD</div>
    <div ref="container" class="pane-chart"></div>
  </div>
</template>

<style scoped>
.macd-pane { position: relative; }
.pane-label {
  position: absolute;
  top: 4px;
  left: 8px;
  font-size: 0.75rem;
  color: #787B86;
  z-index: 1;
}
.pane-chart { height: 150px; }
</style>
