## Why

The trading dashboard currently truncates all timestamps to `YYYY-MM-DD` and only offers daily, weekly, and monthly intervals. The backend already supports intraday intervals (1m, 5m, 15m, 30m, 1h) and returns full ISO 8601 timestamps, but the frontend discards sub-day precision. Users need intraday charts to analyze price action within a trading day.

## What Changes

- Replace the `toTime()` helper (and inline equivalents in RSI/MACD panes) to pass Unix timestamps instead of date-only strings, enabling lightweight-charts to render sub-day precision on the time axis.
- Add intraday intervals (`1m`, `5m`, `15m`, `30m`, `1h`) to the ControlBar interval dropdown.
- Add interval-period validation logic so invalid combinations (e.g., 1m interval with 5y period) are prevented in the UI.

## Capabilities

### New Capabilities

_None — this change extends existing capabilities._

### Modified Capabilities

- `dashboard-app`: The interval selector requirement changes to include intraday intervals (`1m`, `5m`, `15m`, `30m`, `1h`) and adds period-interval compatibility filtering.
- `candlestick-chart`: The time axis rendering requirement changes to support sub-day timestamps via Unix epoch seconds instead of date-only strings.

## Impact

- **Frontend components**: `PriceChart.vue`, `RsiPane.vue`, `MacdPane.vue` — `toTime()` conversion logic changes.
- **Frontend controls**: `ControlBar.vue` — interval list expands, period-interval validation added.
- **No backend changes** — the API already supports all intraday intervals and returns full ISO timestamps.
- **No dependency changes** — lightweight-charts natively supports Unix timestamps for sub-day precision.
