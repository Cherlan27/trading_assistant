## 1. Backend: Technical Indicators Endpoint

- [x] 1.1 Create `yfinance_api/schemas/indicators.py` with Pydantic models: `IndicatorDataPoint(date, value)`, `MACDDataPoint(date, macd, signal, histogram)`, `BollingerDataPoint(date, upper, middle, lower)`, and `IndicatorsResponse` (dict-like model keyed by indicator name)
- [x] 1.2 Create `yfinance_api/services/indicator_service.py` with methods to compute SMA, EMA, RSI, MACD, and Bollinger Bands from a pandas DataFrame using rolling/ewm operations
- [x] 1.3 Create `yfinance_api/routers/indicators.py` with `GET /indicators/{symbol}` endpoint accepting `period`, `interval`, and `indicators` (comma-separated) query parameters. Parse indicator identifiers, fetch OHLCV via `YFinanceService`, compute requested indicators, return `IndicatorsResponse`
- [x] 1.4 Validate indicator identifiers — return HTTP 422 for unrecognized indicator names or invalid formats
- [x] 1.5 Register the indicators router in `yfinance_api/main.py`

## 2. Backend: CORS Middleware

- [x] 2.1 Add `CORSMiddleware` to `yfinance_api/main.py` allowing origin `http://localhost:5173`, all methods, and all headers

## 3. Frontend: Vue 3 Project Scaffolding

- [x] 3.1 Scaffold Vue 3 + TypeScript project with Vite in `dashboard/` directory (`npm create vue@latest`)
- [x] 3.2 Install `lightweight-charts` as a dependency
- [x] 3.3 Configure Vite proxy in `vite.config.ts` to forward `/history`, `/quote`, `/info`, `/indicators`, `/health` requests to `http://localhost:8000`
- [x] 3.4 Clean up scaffolded boilerplate — remove default components, styles, and assets

## 4. Frontend: API Composable

- [x] 4.1 Create `src/composables/useApi.ts` with typed fetch functions: `fetchHistory(symbol, period, interval)` and `fetchIndicators(symbol, period, interval, indicators[])`
- [x] 4.2 Add in-memory cache keyed by `{symbol}:{period}:{interval}` — return cached data when available, invalidate on period/interval change
- [x] 4.3 Add error handling — return error state for 404/502/network failures without throwing

## 5. Frontend: Controls Component

- [x] 5.1 Create `src/components/ControlBar.vue` with symbol text input and "Add" button — emits `add-symbol` on Enter/click
- [x] 5.2 Add symbol chip/tag display with remove buttons — emits `remove-symbol` on click
- [x] 5.3 Add period dropdown (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max) with default `1y` — emits `update:period`
- [x] 5.4 Add interval dropdown (1d, 1wk, 1mo) with default `1d` — emits `update:interval`
- [x] 5.5 Add indicator toggle buttons (SMA(20), SMA(50), EMA(20), RSI(14), MACD, Bollinger(20,2)) — emits `update:indicators`

## 6. Frontend: Candlestick Chart Component

- [x] 6.1 Create `src/components/PriceChart.vue` — initialize a Lightweight Charts instance, create a candlestick series, accept OHLCV data as a prop and render it
- [x] 6.2 Add volume histogram series below the candlestick with green/red color coding matching candle direction
- [x] 6.3 Add crosshair with `subscribeCrosshairMove` — emit hovered data point for the legend
- [x] 6.4 Handle chart resize on container size changes using `ResizeObserver`

## 7. Frontend: Multi-Symbol Overlay

- [x] 7.1 When a second symbol is added, create a line series on the price chart with a distinct color
- [x] 7.2 Implement percentage-change normalization — transform absolute prices to percentage change from the first data point in the visible range
- [x] 7.3 Manage series lifecycle — add/remove line series as symbols are added/removed

## 8. Frontend: Indicator Overlays

- [x] 8.1 Render SMA, EMA line series on the price pane when toggled on — use distinct colors per indicator
- [x] 8.2 Render Bollinger Bands as three line series (upper, middle, lower) on the price pane
- [x] 8.3 Create a separate synchronized chart instance for RSI sub-pane with 0-100 y-axis scale — sync time axis with the main chart via `subscribeVisibleTimeRangeChange`
- [x] 8.4 Create a separate synchronized chart instance for MACD sub-pane with MACD line, signal line, and histogram bars — sync time axis with the main chart
- [x] 8.5 Show/hide sub-panes dynamically based on indicator toggle state

## 9. Frontend: Legend Component

- [x] 9.1 Create `src/components/ChartLegend.vue` displaying color-coded entries for each active symbol and indicator
- [x] 9.2 Update legend values on crosshair move — show OHLCV for the primary symbol and values for active indicators at the hovered time point

## 10. Frontend: App Integration

- [x] 10.1 Wire up `App.vue` — compose ControlBar, PriceChart, sub-pane charts, and ChartLegend with shared state via a `useChartState` composable
- [x] 10.2 Implement data flow: on symbol add → fetch history + indicators in parallel → pass to chart components
- [x] 10.3 Implement period/interval change → re-fetch all data for all symbols → redraw charts
- [x] 10.4 Add toast notification for errors (invalid symbol, network failure) — a simple auto-dismissing message

## 11. Smoke Test

- [x] 11.1 Start both backend (`uvicorn`) and frontend (`npm run dev`), verify the dashboard loads
- [x] 11.2 Add a symbol (AAPL), verify candlestick + volume chart renders
- [x] 11.3 Add a second symbol (MSFT), verify line overlay appears with percentage normalization
- [x] 11.4 Toggle SMA(20) and RSI(14), verify overlay and sub-pane render
- [x] 11.5 Change period to 3mo, verify chart re-fetches and redraws
- [x] 11.6 Enter an invalid symbol, verify toast error appears and chart is unaffected
