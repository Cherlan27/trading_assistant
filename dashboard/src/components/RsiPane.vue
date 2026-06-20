<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { createChart, LineSeries } from 'lightweight-charts'
import type { IChartApi, ISeriesApi, Time } from 'lightweight-charts'
import type { IndicatorDataPoint } from '@/composables/useApi'

const props = defineProps<{
  data: IndicatorDataPoint[] | null
  visibleRange: { from: Time; to: Time } | null
}>()

const container = ref<HTMLDivElement>()
let chart: IChartApi | null = null
let rsiSeries: ISeriesApi<'Line'> | null = null
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

  rsiSeries = chart.addSeries(LineSeries, {
    color: '#E040FB',
    lineWidth: 1,
    priceFormat: { type: 'custom', formatter: (v: number) => v.toFixed(0) },
  })

  rsiSeries.createPriceLine({ price: 70, color: '#787B86', lineWidth: 1, lineStyle: 2 })
  rsiSeries.createPriceLine({ price: 30, color: '#787B86', lineWidth: 1, lineStyle: 2 })

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
  if (!rsiSeries || !props.data) return
  rsiSeries.setData(props.data.map(d => ({
    time: d.date.slice(0, 10) as unknown as Time,
    value: d.value,
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
  <div class="rsi-pane">
    <div class="pane-label">RSI(14)</div>
    <div ref="container" class="pane-chart"></div>
  </div>
</template>

<style scoped>
.rsi-pane { position: relative; }
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
