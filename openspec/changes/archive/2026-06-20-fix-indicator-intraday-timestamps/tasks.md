## 1. Fix date formatting in indicator_service.py

- [x] 1.1 Replace `str(df.index[i].date())` with `df.index[i].isoformat()` in `compute_macd()` (line 42)
- [x] 1.2 Replace `str(df.index[i].date())` with `df.index[i].isoformat()` in `compute_bbands()` (line 62)
- [x] 1.3 Replace `str(df.index[i].date())` with `df.index[i].isoformat()` in `_to_data_points()` (line 77)

## 2. Verify

- [x] 2.1 Start the API server and confirm `/indicators/AAPL?period=1d&interval=5m&indicators=sma_20` returns full ISO-8601 timestamps
- [x] 2.2 Start the dashboard and confirm indicators render correctly for an intraday interval (e.g., period=1d, interval=5m)
- [x] 2.3 Confirm indicators still render correctly for daily interval (period=1y, interval=1d)
