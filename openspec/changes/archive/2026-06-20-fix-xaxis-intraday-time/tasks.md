## 1. Add isIntraday helper

- [x] 1.1 Add `isIntraday(interval: string): boolean` function to `dashboard/src/constants.ts` that returns `true` for intervals `1m`, `5m`, `15m`, `30m`, `1h`

## 2. Pass interval prop to PriceChart

- [x] 2.1 Add `interval` to the props interface in `dashboard/src/components/PriceChart.vue`
- [x] 2.2 Pass `:interval="state.interval.value"` to the `<PriceChart>` component in `dashboard/src/App.vue`

## 3. Toggle timeVisible on the timeScale

- [x] 3.1 Add a `watch` on the `interval` prop in `PriceChart.vue` that calls `chart.timeScale().applyOptions({ timeVisible: isIntraday(interval) })` with `{ immediate: true }`

## 4. Verify

- [x] 4.1 Start the dev server, select an intraday interval (e.g. period "1d", interval "5m"), and confirm the x-axis shows hours and minutes
- [x] 4.2 Switch to a daily interval (e.g. period "1y", interval "1d") and confirm the x-axis shows dates only
