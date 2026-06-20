## Why

The dashboard's x-axis only shows dates (days) even when an intraday interval (1m, 5m, 15m, 30m, 1h) is selected. Users cannot see hours and minutes on the time axis, making intraday charts unreadable. The candlestick-chart spec already requires "the time axis showing hours and minutes within the trading day" for intraday intervals, but the implementation is missing the `timeVisible` configuration on the lightweight-charts timeScale.

## What Changes

- Pass the current `interval` value as a prop to `PriceChart.vue` so it knows whether the data is intraday
- Set `timeVisible: true` on the lightweight-charts `timeScale` when an intraday interval is active
- Set `timeVisible: false` for daily/weekly/monthly intervals to keep the current clean date-only display

## Capabilities

### New Capabilities

_(none — this is a bugfix for existing capability)_

### Modified Capabilities

- `candlestick-chart`: The time scale must dynamically toggle `timeVisible` based on the active interval, fulfilling the existing intraday scenario requirement

## Impact

- `dashboard/src/components/PriceChart.vue`: Receives new `interval` prop, adds reactive timeScale configuration
- `dashboard/src/App.vue`: Passes `interval` prop down to `PriceChart`
- No API changes, no new dependencies
