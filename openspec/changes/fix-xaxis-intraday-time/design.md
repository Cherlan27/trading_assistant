## Context

The dashboard uses TradingView Lightweight Charts to render candlestick data. The `toTime()` helper in `constants.ts` already converts ISO date strings to Unix epoch seconds (`UTCTimestamp`), which correctly preserves intraday time information. However, the chart's `timeScale` is configured with only `borderColor` — it never sets `timeVisible: true`, which lightweight-charts requires to display hours and minutes on the x-axis. Additionally, `PriceChart.vue` does not receive the current `interval` prop, so it cannot determine whether intraday time display is appropriate.

## Goals / Non-Goals

**Goals:**
- Show hours and minutes on the x-axis when an intraday interval is selected (1m, 5m, 15m, 30m, 1h)
- Keep date-only display for daily and longer intervals (1d, 1wk, 1mo)
- Dynamically switch between modes when the user changes the interval

**Non-Goals:**
- Changing the time data format or the `toTime()` conversion function (it already works correctly)
- Modifying the API response format
- Adding seconds-level precision to the time axis

## Decisions

### Decision 1: Pass `interval` prop to PriceChart

`App.vue` already has access to `state.interval.value` but does not pass it to `PriceChart`. Adding it as a prop is the simplest way to give the chart component the context it needs.

**Alternative considered**: Deriving intraday-ness from the data itself (e.g., checking if multiple data points fall on the same day). Rejected because it's fragile and adds unnecessary computation — the interval is already known.

### Decision 2: Use `chart.timeScale().applyOptions()` reactively

A `watch` on the `interval` prop will call `chart.timeScale().applyOptions({ timeVisible })` whenever the interval changes. This is the standard lightweight-charts API for updating chart options at runtime without recreating the chart.

**Alternative considered**: Destroying and recreating the chart on interval change. Rejected because `applyOptions` is designed for exactly this use case and avoids the overhead of full chart recreation.

### Decision 3: Intraday detection via helper function

A simple helper `isIntraday(interval: string): boolean` in `constants.ts` checks against the set `['1m', '5m', '15m', '30m', '1h']`. This keeps the logic centralized and reusable (the RSI and MACD sub-panes may also benefit from it later).

## Risks / Trade-offs

- **[Low] Time zone display**: lightweight-charts renders UTC timestamps by default. Intraday market data from yfinance includes timezone offsets, and `toTime()` converts via `new Date().getTime()` which handles this correctly. No additional timezone handling needed.
- **[Low] Initial render timing**: The `timeVisible` option must be applied after chart creation. The `watch` with `{ immediate: true }` ensures correct state on first render.
