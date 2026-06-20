<script setup lang="ts">
import { computed, ref } from 'vue'
import ControlBar from '@/components/ControlBar.vue'
import PriceChart from '@/components/PriceChart.vue'
import RsiPane from '@/components/RsiPane.vue'
import MacdPane from '@/components/MacdPane.vue'
import ChartLegend from '@/components/ChartLegend.vue'
import { useChartState } from '@/composables/useChartState'
import { OVERLAY_COLORS, INDICATOR_COLORS } from '@/constants'
import type { IndicatorDataPoint, MACDDataPoint } from '@/composables/useApi'

const state = useChartState()
const visibleRange = ref<any>(null)

const primarySymbol = computed(() => state.symbols.value[0] || '')

const primaryData = computed(() => {
  const sym = primarySymbol.value
  return sym ? (state.symbolData.value.get(sym)?.history ?? null) : null
})

const overlaySymbols = computed(() =>
  state.symbols.value.slice(1)
    .map(sym => ({
      symbol: sym,
      data: state.symbolData.value.get(sym)?.history ?? [],
    }))
    .filter(o => o.data.length > 0),
)

const primaryIndicators = computed(() => {
  const sym = primarySymbol.value
  if (!sym) return {}
  return state.symbolData.value.get(sym)?.indicators ?? {}
})

const rsiData = computed<IndicatorDataPoint[] | null>(() => {
  if (!state.activeIndicators.value.includes('rsi_14')) return null
  return (primaryIndicators.value['rsi_14'] as IndicatorDataPoint[]) ?? null
})

const macdData = computed<MACDDataPoint[] | null>(() => {
  if (!state.activeIndicators.value.includes('macd')) return null
  return (primaryIndicators.value['macd'] as MACDDataPoint[]) ?? null
})

const showRsi = computed(() => state.activeIndicators.value.includes('rsi_14') && rsiData.value !== null)
const showMacd = computed(() => state.activeIndicators.value.includes('macd') && macdData.value !== null)

const overlayColorMap = computed(() => {
  const colors: Record<string, string> = {}
  state.symbols.value.slice(1).forEach((sym, idx) => {
    colors[sym] = OVERLAY_COLORS[idx % OVERLAY_COLORS.length]
  })
  return colors
})

function onCrosshairMove(data: any) {
  state.crosshairInfo.value = data
}
</script>

<template>
  <div id="app">
    <ControlBar
      :symbols="state.symbols.value"
      :period="state.period.value"
      :interval="state.interval.value"
      :active-indicators="state.activeIndicators.value"
      @add-symbol="state.addSymbol"
      @remove-symbol="state.removeSymbol"
      @update:period="state.setPeriod"
      @update:interval="state.setInterval"
      @update:indicators="state.setIndicators"
    />

    <div class="chart-area">
      <PriceChart
        v-if="primarySymbol"
        :primary-symbol="primarySymbol"
        :primary-data="primaryData"
        :overlay-symbols="overlaySymbols"
        :indicators="primaryIndicators"
        :active-indicators="state.activeIndicators.value"
        @crosshair-move="onCrosshairMove"
        @visible-range-change="(r: any) => visibleRange = r"
      />
      <div v-else class="empty-state">Enter a ticker symbol above to get started</div>

      <RsiPane
        v-if="showRsi"
        :data="rsiData"
        :visible-range="visibleRange"
      />

      <MacdPane
        v-if="showMacd"
        :data="macdData"
        :visible-range="visibleRange"
      />
    </div>

    <ChartLegend
      v-if="primarySymbol"
      :primary-symbol="primarySymbol"
      :overlay-symbols="state.symbols.value.slice(1)"
      :active-indicators="state.activeIndicators.value"
      :crosshair-data="state.crosshairInfo.value"
      :overlay-colors="overlayColorMap"
      :indicator-colors="INDICATOR_COLORS"
    />

    <div class="toast-container">
      <div v-for="toast in state.toasts.value" :key="toast.id" class="toast">
        {{ toast.message }}
      </div>
    </div>

    <div v-if="state.loading.value" class="loading-indicator">Loading...</div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background: #1a1a2e;
  color: #e0e0e0;
}

#app {
  padding: 1rem;
  height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chart-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #787B86;
  font-size: 1.1rem;
}

.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 100;
}

.toast {
  padding: 0.75rem 1.25rem;
  background: #ef5350;
  color: white;
  border-radius: 6px;
  font-size: 0.9rem;
  animation: toast-in 0.3s ease-out;
}

@keyframes toast-in {
  from { opacity: 0; transform: translateX(100%); }
  to { opacity: 1; transform: translateX(0); }
}

.loading-indicator {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  background: #0f3460;
  border-radius: 6px;
  font-size: 0.85rem;
  color: #a0a0a0;
}
</style>
