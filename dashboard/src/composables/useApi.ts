export interface OHLCVDataPoint {
  date: string
  open: number
  high: number
  low: number
  close: number
  volume: number
}

export interface HistoryResponse {
  symbol: string
  data: OHLCVDataPoint[]
}

export interface IndicatorDataPoint {
  date: string
  value: number
}

export interface MACDDataPoint {
  date: string
  macd: number
  signal: number
  histogram: number
}

export interface BollingerDataPoint {
  date: string
  upper: number
  middle: number
  lower: number
}

export type IndicatorData = IndicatorDataPoint[] | MACDDataPoint[] | BollingerDataPoint[]

export interface IndicatorsResponse {
  symbol: string
  indicators: Record<string, IndicatorData>
}

export interface ApiResult<T> {
  data: T | null
  error: string | null
}

const historyCache = new Map<string, HistoryResponse>()
const indicatorCache = new Map<string, IndicatorsResponse>()

function cacheKey(symbol: string, period: string, interval: string): string {
  return `${symbol}:${period}:${interval}`
}

export function clearCache() {
  historyCache.clear()
  indicatorCache.clear()
}

export async function fetchHistory(
  symbol: string,
  period: string,
  interval: string,
): Promise<ApiResult<HistoryResponse>> {
  const key = cacheKey(symbol, period, interval)
  const cached = historyCache.get(key)
  if (cached) return { data: cached, error: null }

  try {
    const res = await fetch(`/history/${symbol}?period=${period}&interval=${interval}`)
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      return { data: null, error: body.detail || `Error ${res.status}` }
    }
    const data: HistoryResponse = await res.json()
    historyCache.set(key, data)
    return { data, error: null }
  } catch {
    return { data: null, error: 'Network error — is the API server running?' }
  }
}

export async function fetchIndicators(
  symbol: string,
  period: string,
  interval: string,
  indicators: string[],
): Promise<ApiResult<IndicatorsResponse>> {
  if (indicators.length === 0) {
    return { data: { symbol, indicators: {} }, error: null }
  }

  const key = `${cacheKey(symbol, period, interval)}:${indicators.sort().join(',')}`
  const cached = indicatorCache.get(key)
  if (cached) return { data: cached, error: null }

  try {
    const params = new URLSearchParams({
      period,
      interval,
      indicators: indicators.join(','),
    })
    const res = await fetch(`/indicators/${symbol}?${params}`)
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      return { data: null, error: body.detail || `Error ${res.status}` }
    }
    const data: IndicatorsResponse = await res.json()
    indicatorCache.set(key, data)
    return { data, error: null }
  } catch {
    return { data: null, error: 'Network error — is the API server running?' }
  }
}
