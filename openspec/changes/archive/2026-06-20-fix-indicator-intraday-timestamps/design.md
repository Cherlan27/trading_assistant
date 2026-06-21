## Context

The indicator service (`indicator_service.py`) formats all data point dates using `str(df.index[i].date())`, which strips the time component from the pandas DatetimeIndex. The history service (`yfinance_service.py`) correctly uses `index.isoformat()`. For daily intervals this works by coincidence — one point per day means no collisions. For intraday intervals (1m–1h), dozens of points collapse to the same date string, breaking chart rendering.

## Goals / Non-Goals

**Goals:**
- Indicator date format matches history date format for all intervals
- Indicators render correctly for intraday intervals (1m, 5m, 15m, 30m, 1h)

**Non-Goals:**
- Changing the indicator computation logic
- Modifying the frontend date parsing (already handles both formats)
- Adding new indicators or intervals

## Decisions

### Use `.isoformat()` on the DatetimeIndex directly

Replace `str(df.index[i].date())` with `df.index[i].isoformat()` in all three locations within `indicator_service.py`.

**Why this over alternatives:**
- **Alternative: `str(df.index[i])`** — produces format like `2024-01-15 10:30:00+00:00` (space-separated), which is not ISO-8601 compliant and may parse inconsistently across browsers.
- **Alternative: `.strftime()`** — requires choosing a format string and handling timezone-aware vs naive datetimes. Over-engineered for this case.
- **`.isoformat()`** — produces standard ISO-8601 (`2024-01-15T10:30:00+00:00`), matches what `yfinance_service.py` already uses, and `new Date()` in JavaScript parses it reliably.

## Risks / Trade-offs

- **[API response format change]** → The `date` field changes from `"2024-01-15"` to `"2024-01-15T00:00:00+00:00"` for daily intervals. The frontend `toTime()` handles both via `new Date().getTime()`, so no breakage. Any external consumers would need to handle ISO-8601 datetime strings, which is standard practice.
