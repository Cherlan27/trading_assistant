## 1. Shared Time Utility

- [ ] 1.1 Create a `toTime()` utility function that converts ISO 8601 date strings to Unix epoch seconds (`Math.floor(new Date(isoString).getTime() / 1000)`) and returns it typed as `Time` from lightweight-charts
- [ ] 1.2 Replace the `toTime()` function in `PriceChart.vue` with an import of the shared utility
- [ ] 1.3 Replace the inline `d.date.slice(0, 10) as unknown as Time` in `RsiPane.vue` with the shared utility
- [ ] 1.4 Replace the inline `d.slice(0, 10) as unknown as Time` in `MacdPane.vue` with the shared utility

## 2. Period-Interval Compatibility

- [ ] 2.1 Define a `PERIOD_INTERVAL_MAP` constant that maps each period to its array of valid intervals based on yfinance constraints
- [ ] 2.2 Export a `getValidIntervals(period: string): string[]` helper that returns the valid intervals for a given period

## 3. ControlBar Intraday Intervals

- [ ] 3.1 Expand the `intervals` array in `ControlBar.vue` to include `1m`, `5m`, `15m`, `30m`, `1h` alongside existing `1d`, `1wk`, `1mo`
- [ ] 3.2 Add a computed property that filters the interval dropdown options using `getValidIntervals(period)`
- [ ] 3.3 Emit an `update:interval` event with the first valid interval when the current interval becomes invalid after a period change

## 4. Verification

- [ ] 4.1 Run TypeScript type checking (`npm run build` or `vue-tsc`) to ensure no type errors
- [ ] 4.2 Manually verify daily chart (e.g., AAPL 1y/1d) renders correctly with Unix timestamps
- [ ] 4.3 Manually verify intraday chart (e.g., AAPL 1d/5m) shows sub-day candles with hour/minute axis labels
