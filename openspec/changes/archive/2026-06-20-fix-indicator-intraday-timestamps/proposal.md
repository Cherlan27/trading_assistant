## Why

Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands) are broken for all intraday intervals (1m, 5m, 15m, 30m, 1h). The indicator service formats dates with `.date()` which strips the time component, while the history service uses `.isoformat()` preserving it. This causes all intraday data points within the same day to collapse to the same timestamp, producing duplicate keys that lightweight-charts cannot render.

## What Changes

- Fix date formatting in `IndicatorService` to use `.isoformat()` instead of `.date()`, matching the existing pattern in `YFinanceService`
- Affects three code paths: `_to_data_points()` (SMA, EMA, RSI), `compute_macd()`, and `compute_bbands()`

## Capabilities

### New Capabilities

_None — this is a bug fix._

### Modified Capabilities

- `technical-indicators-api`: The `date` field in indicator response data points must preserve full ISO-8601 timestamps (including time) for intraday intervals, matching the format used by the `/history` endpoint.

## Impact

- **Code**: `yfinance_api/services/indicator_service.py` — three lines changed
- **API**: The `date` field in indicator responses will change from `"2024-01-15"` to `"2024-01-15T10:30:00+00:00"` for intraday intervals. Daily intervals remain unaffected since `.isoformat()` on a daily index still produces a full datetime.
- **Frontend**: No changes needed — `toTime()` in `constants.ts` already parses both formats correctly via `new Date(date).getTime()`
