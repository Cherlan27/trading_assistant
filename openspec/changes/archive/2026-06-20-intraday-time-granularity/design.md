## Context

The trading dashboard uses TradingView Lightweight Charts to render OHLCV candlestick data. The backend (yfinance FastAPI service) already supports intraday intervals (`1m`, `5m`, `15m`, `30m`, `1h`, etc.) and returns full ISO 8601 timestamps with sub-day precision. However, the frontend's `toTime()` function truncates timestamps to `YYYY-MM-DD` (date-only strings), and the ControlBar only exposes `1d`, `1wk`, `1mo` intervals. This means intraday data cannot be displayed even though it's available.

## Goals / Non-Goals

**Goals:**
- Enable intraday chart viewing with minute/hour granularity on the time axis
- Preserve correct rendering for daily and longer intervals
- Prevent users from selecting invalid period-interval combinations

**Non-Goals:**
- Real-time streaming / live data updates
- Custom interval input (only preset values)
- Backend API changes (already supports all needed intervals)

## Decisions

### Decision 1: Use Unix timestamps for lightweight-charts Time type

**Choice:** Convert ISO strings to Unix epoch seconds via `Math.floor(new Date(isoString).getTime() / 1000)` and use lightweight-charts' `UTCTimestamp` time type.

**Why:** Lightweight-charts accepts two time formats: `YYYY-MM-DD` strings (date only, no sub-day precision) or Unix timestamps in seconds (full precision). Since we need sub-day data, Unix timestamps are the only viable option. This also works correctly for daily data — a date like `2024-01-15T00:00:00` converts to a midnight timestamp that renders identically to the date string.

**Alternative considered:** Passing ISO strings directly — not supported by lightweight-charts' `Time` type.

### Decision 2: Centralize toTime() as a shared utility

**Choice:** Extract `toTime()` from `PriceChart.vue` into a shared utility (e.g., a composable or constants file) and replace the inline `date.slice(0, 10)` equivalents in `RsiPane.vue` and `MacdPane.vue`.

**Why:** All three chart components need the same conversion. A single source prevents divergence and makes the change a one-line update.

### Decision 3: Static period-interval compatibility map

**Choice:** Define a lookup object mapping each period to its valid intervals. The ControlBar filters the interval dropdown options based on the selected period.

**Why:** yfinance enforces its own period-interval constraints (e.g., 1m data is only available for the last 7 days). Filtering in the UI prevents confusing API errors. A static map is simple and matches yfinance's known constraints without needing a server round-trip.

Compatibility rules (based on yfinance limits):
- `1d`, `5d` → `1m`, `5m`, `15m`, `30m`, `1h`, `1d`
- `1mo` → `5m`, `15m`, `30m`, `1h`, `1d`
- `3mo`, `6mo` → `1h`, `1d`, `1wk`
- `1y`, `2y` → `1d`, `1wk`, `1mo`
- `5y`, `max` → `1d`, `1wk`, `1mo`

### Decision 4: Auto-adjust interval on period change

**Choice:** When the user changes the period and the current interval is no longer valid, auto-select the first valid interval for the new period.

**Why:** Avoids a broken state where the selected interval is incompatible with the period. Auto-selection to the highest-granularity valid option gives users the most detailed view by default.

## Risks / Trade-offs

- **yfinance rate limits on intraday data** → Intraday requests fetch more data points. Existing client-side caching mitigates repeated requests. No additional mitigation needed for now.
- **Compatibility map may drift from yfinance behavior** → yfinance could change its constraints. The static map is easy to update and matches current documented behavior. If a request fails, the existing error toast handles it gracefully.
- **Timezone display** → lightweight-charts renders UTC timestamps by default. Intraday users may expect local time. This is acceptable for v1; a timezone selector could be added later without architectural changes.
