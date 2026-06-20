## Why

The yfinance FastAPI service provides raw market data endpoints but no way to visualize it. A dashboard is needed to render stock time series as interactive candlestick charts, compare multiple symbols, and overlay technical indicators — turning the API from a data pipe into a usable analysis tool.

## What Changes

- Add a Vue 3 + Vite + TypeScript single-page dashboard application in `dashboard/`
- Add a `/indicators/{symbol}` endpoint to the FastAPI backend for server-side technical indicator computation (SMA, EMA, RSI, MACD, Bollinger Bands)
- Add CORS middleware to the FastAPI app to allow the frontend dev server to call the API
- Integrate TradingView Lightweight Charts for financial chart rendering

## Capabilities

### New Capabilities
- `dashboard-app`: Vue 3 + Vite application scaffolding, dev server with API proxy, and single-page layout with controls, chart area, and legend
- `candlestick-chart`: Candlestick + volume chart rendering using Lightweight Charts, with crosshair and hover data display
- `multi-symbol-comparison`: Overlay multiple ticker symbols on the same chart using percentage-change normalization
- `technical-indicators-api`: FastAPI endpoint computing SMA, EMA, RSI, MACD, and Bollinger Bands from OHLCV data using pandas
- `indicator-overlays`: Frontend rendering of technical indicators as line series on the price pane or in separate sub-panes (RSI, MACD)

### Modified Capabilities
- `fastapi-app`: Adding CORS middleware and registering the indicators router

## Impact

- **New directory:** `dashboard/` with Vue 3 project (package.json, vite config, src/)
- **New backend files:** indicators router, indicator schemas, indicator computation service
- **Modified:** `yfinance_api/main.py` — CORS middleware and indicators router registration
- **New dependency:** pandas is already available transitively via yfinance; no new Python deps. Frontend adds `lightweight-charts` as an npm dependency
- **Dev workflow:** Two processes during development (uvicorn + vite dev)
