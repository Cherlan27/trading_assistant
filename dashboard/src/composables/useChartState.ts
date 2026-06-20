import { ref } from 'vue'
import {
  fetchHistory, fetchIndicators, clearCache,
  type OHLCVDataPoint, type IndicatorData,
} from './useApi'

export interface SymbolData {
  history: OHLCVDataPoint[]
  indicators: Record<string, IndicatorData>
}

export interface Toast {
  id: number
  message: string
}

export interface CrosshairInfo {
  time: string
  ohlcv?: { open: number; high: number; low: number; close: number; volume: number }
  indicatorValues: Record<string, number>
}

let toastId = 0

export function useChartState() {
  const symbols = ref<string[]>([])
  const period = ref('1y')
  const interval = ref('1d')
  const activeIndicators = ref<string[]>([])
  const symbolData = ref(new Map<string, SymbolData>())
  const loading = ref(false)
  const toasts = ref<Toast[]>([])
  const crosshairInfo = ref<CrosshairInfo | null>(null)

  function showToast(message: string) {
    const id = ++toastId
    toasts.value.push({ id, message })
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, 4000)
  }

  async function fetchSymbolData(symbol: string) {
    const [histResult, indResult] = await Promise.all([
      fetchHistory(symbol, period.value, interval.value),
      activeIndicators.value.length > 0
        ? fetchIndicators(symbol, period.value, interval.value, activeIndicators.value)
        : Promise.resolve({ data: { symbol, indicators: {} as Record<string, IndicatorData> }, error: null }),
    ])

    if (histResult.error) {
      showToast(`${symbol}: ${histResult.error}`)
      return null
    }

    const indicators = indResult.data?.indicators ?? {}
    if (indResult.error) {
      showToast(`${symbol} indicators: ${indResult.error}`)
    }

    return { history: histResult.data!.data, indicators }
  }

  async function addSymbol(symbol: string) {
    if (symbols.value.includes(symbol)) return
    symbols.value = [...symbols.value, symbol]
    loading.value = true
    const data = await fetchSymbolData(symbol)
    loading.value = false
    if (data) {
      symbolData.value.set(symbol, data)
      symbolData.value = new Map(symbolData.value)
    } else {
      symbols.value = symbols.value.filter(s => s !== symbol)
    }
  }

  function removeSymbol(symbol: string) {
    symbols.value = symbols.value.filter(s => s !== symbol)
    symbolData.value.delete(symbol)
    symbolData.value = new Map(symbolData.value)
  }

  async function refetchAll() {
    clearCache()
    loading.value = true
    const entries = await Promise.all(
      symbols.value.map(async sym => {
        const data = await fetchSymbolData(sym)
        return [sym, data] as const
      }),
    )
    loading.value = false
    const newMap = new Map<string, SymbolData>()
    for (const [sym, data] of entries) {
      if (data) newMap.set(sym, data)
    }
    symbolData.value = newMap
  }

  function setPeriod(p: string) {
    period.value = p
    refetchAll()
  }

  function setInterval(i: string) {
    interval.value = i
    refetchAll()
  }

  async function setIndicators(inds: string[]) {
    activeIndicators.value = inds
    if (symbols.value.length === 0) return

    loading.value = true
    const updates = await Promise.all(
      symbols.value.map(async sym => {
        const result = await fetchIndicators(sym, period.value, interval.value, inds)
        return [sym, result] as const
      }),
    )
    loading.value = false

    for (const [sym, result] of updates) {
      const existing = symbolData.value.get(sym)
      if (existing && result.data) {
        existing.indicators = result.data.indicators
      } else if (result.error) {
        showToast(`${sym} indicators: ${result.error}`)
      }
    }
    symbolData.value = new Map(symbolData.value)
  }

  return {
    symbols, period, interval, activeIndicators,
    symbolData, loading, toasts, crosshairInfo,
    addSymbol, removeSymbol, setPeriod, setInterval, setIndicators, showToast,
  }
}
