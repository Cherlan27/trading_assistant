import type { Time } from 'lightweight-charts'

export function toTime(date: string): Time {
  return Math.floor(new Date(date).getTime() / 1000) as unknown as Time
}

export const ALL_INTERVALS = ['1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo'] as const

export const PERIOD_INTERVAL_MAP: Record<string, string[]> = {
  '1d':  ['1m', '5m', '15m', '30m', '1h', '1d'],
  '5d':  ['1m', '5m', '15m', '30m', '1h', '1d'],
  '1mo': ['5m', '15m', '30m', '1h', '1d'],
  '3mo': ['1h', '1d', '1wk'],
  '6mo': ['1h', '1d', '1wk'],
  '1y':  ['1d', '1wk', '1mo'],
  '2y':  ['1d', '1wk', '1mo'],
  '5y':  ['1d', '1wk', '1mo'],
  'max': ['1d', '1wk', '1mo'],
}

export function getValidIntervals(period: string): string[] {
  return PERIOD_INTERVAL_MAP[period] ?? ['1d', '1wk', '1mo']
}

export const OVERLAY_COLORS = ['#2962FF', '#FF6D00', '#AB47BC', '#26A69A', '#D50000']

export const INDICATOR_COLORS: Record<string, string> = {
  sma_20: '#FF9800',
  sma_50: '#2196F3',
  ema_20: '#4CAF50',
  rsi_14: '#E040FB',
  macd: '#2962FF',
  bbands_20: '#787B86',
  bbands_20_upper: '#787B86',
  bbands_20_middle: '#2962FF',
  bbands_20_lower: '#787B86',
}
