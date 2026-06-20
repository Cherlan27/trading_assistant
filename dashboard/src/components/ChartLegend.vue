<script setup lang="ts">
import type { CrosshairInfo } from '@/composables/useChartState'

defineProps<{
  primarySymbol: string
  overlaySymbols: string[]
  activeIndicators: string[]
  crosshairData: CrosshairInfo | null
  overlayColors: Record<string, string>
  indicatorColors: Record<string, string>
}>()

const INDICATOR_LABELS: Record<string, string> = {
  sma_20: 'SMA(20)',
  sma_50: 'SMA(50)',
  ema_20: 'EMA(20)',
  rsi_14: 'RSI(14)',
  macd: 'MACD',
  bbands_20: 'BB(20,2)',
}

function formatNum(n: number): string {
  return n >= 1000 ? n.toLocaleString(undefined, { maximumFractionDigits: 2 }) : n.toFixed(2)
}

function formatVolume(v: number): string {
  if (v >= 1e9) return (v / 1e9).toFixed(2) + 'B'
  if (v >= 1e6) return (v / 1e6).toFixed(2) + 'M'
  if (v >= 1e3) return (v / 1e3).toFixed(1) + 'K'
  return v.toString()
}
</script>

<template>
  <div class="chart-legend">
    <div v-if="primarySymbol" class="legend-entry">
      <span class="color-dot" style="background: #26a69a"></span>
      <span class="legend-label">{{ primarySymbol }}</span>
      <span v-if="crosshairData?.ohlcv" class="legend-values">
        O: {{ formatNum(crosshairData.ohlcv.open) }}
        H: {{ formatNum(crosshairData.ohlcv.high) }}
        L: {{ formatNum(crosshairData.ohlcv.low) }}
        C: {{ formatNum(crosshairData.ohlcv.close) }}
        V: {{ formatVolume(crosshairData.ohlcv.volume) }}
      </span>
    </div>

    <div v-for="sym in overlaySymbols" :key="sym" class="legend-entry">
      <span class="color-dot" :style="{ background: overlayColors[sym] || '#fff' }"></span>
      <span class="legend-label">{{ sym }}</span>
      <span v-if="crosshairData?.indicatorValues[`overlay:${sym}`] !== undefined" class="legend-values">
        {{ formatNum(crosshairData!.indicatorValues[`overlay:${sym}`]) }}%
      </span>
    </div>

    <div v-for="ind in activeIndicators" :key="ind" class="legend-entry">
      <span class="color-dot" :style="{ background: indicatorColors[ind] || '#fff' }"></span>
      <span class="legend-label">{{ INDICATOR_LABELS[ind] || ind }}</span>
      <span v-if="crosshairData?.indicatorValues[ind] !== undefined" class="legend-values">
        {{ formatNum(crosshairData!.indicatorValues[ind]) }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 0.5rem 1rem;
  background: #16213e;
  border-radius: 8px;
  font-size: 0.85rem;
}

.legend-entry {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-label { font-weight: 600; }
.legend-values { color: #a0a0a0; }
</style>
