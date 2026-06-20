<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  symbols: string[]
  period: string
  interval: string
  activeIndicators: string[]
}>()

const emit = defineEmits<{
  'add-symbol': [symbol: string]
  'remove-symbol': [symbol: string]
  'update:period': [period: string]
  'update:interval': [interval: string]
  'update:indicators': [indicators: string[]]
}>()

const symbolInput = ref('')

const periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max']
const intervals = ['1d', '1wk', '1mo']

const indicatorOptions = [
  { id: 'sma_20', label: 'SMA(20)' },
  { id: 'sma_50', label: 'SMA(50)' },
  { id: 'ema_20', label: 'EMA(20)' },
  { id: 'rsi_14', label: 'RSI(14)' },
  { id: 'macd', label: 'MACD' },
  { id: 'bbands_20', label: 'BB(20,2)' },
]

function addSymbol() {
  const sym = symbolInput.value.trim().toUpperCase()
  if (sym && !props.symbols.includes(sym)) {
    emit('add-symbol', sym)
    symbolInput.value = ''
  }
}

function toggleIndicator(id: string) {
  const current = [...props.activeIndicators]
  const idx = current.indexOf(id)
  if (idx >= 0) {
    current.splice(idx, 1)
  } else {
    current.push(id)
  }
  emit('update:indicators', current)
}
</script>

<template>
  <div class="control-bar">
    <div class="symbol-section">
      <form class="symbol-input" @submit.prevent="addSymbol">
        <input
          v-model="symbolInput"
          type="text"
          placeholder="Add symbol (e.g. AAPL)"
        />
        <button type="submit">Add</button>
      </form>
      <div class="chips">
        <span v-for="sym in symbols" :key="sym" class="chip">
          {{ sym }}
          <button class="chip-remove" @click="emit('remove-symbol', sym)">&times;</button>
        </span>
      </div>
    </div>

    <div class="selectors">
      <label>
        Period
        <select :value="period" @change="emit('update:period', ($event.target as HTMLSelectElement).value)">
          <option v-for="p in periods" :key="p" :value="p">{{ p }}</option>
        </select>
      </label>
      <label>
        Interval
        <select :value="interval" @change="emit('update:interval', ($event.target as HTMLSelectElement).value)">
          <option v-for="i in intervals" :key="i" :value="i">{{ i }}</option>
        </select>
      </label>
    </div>

    <div class="indicators">
      <button
        v-for="ind in indicatorOptions"
        :key="ind.id"
        :class="['indicator-btn', { active: activeIndicators.includes(ind.id) }]"
        @click="toggleIndicator(ind.id)"
      >
        {{ ind.label }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.control-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 1rem;
  background: #16213e;
  border-radius: 8px;
  flex-wrap: wrap;
}

.symbol-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.symbol-input {
  display: flex;
  gap: 0.25rem;
}

.symbol-input input {
  padding: 0.4rem 0.6rem;
  border: 1px solid #333;
  border-radius: 4px;
  background: #0f3460;
  color: #e0e0e0;
  width: 160px;
}

.symbol-input button, .selectors select, .indicator-btn {
  padding: 0.4rem 0.6rem;
  border: 1px solid #333;
  border-radius: 4px;
  background: #0f3460;
  color: #e0e0e0;
  cursor: pointer;
}

.chips {
  display: flex;
  gap: 0.25rem;
}

.chip {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: #533483;
  border-radius: 12px;
  font-size: 0.85rem;
}

.chip-remove {
  background: none;
  border: none;
  color: #e0e0e0;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0;
}

.selectors {
  display: flex;
  gap: 0.75rem;
}

.selectors label {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
}

.indicators {
  display: flex;
  gap: 0.35rem;
}

.indicator-btn {
  font-size: 0.8rem;
  transition: background 0.15s;
}

.indicator-btn.active {
  background: #533483;
  border-color: #7b5ea7;
}
</style>
