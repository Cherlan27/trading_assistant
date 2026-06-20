## Context

The yfinance FastAPI service (`yfinance_api/`) provides REST endpoints for stock quotes, ticker info, and historical OHLCV data. It wraps the yfinance Python library and serves data over HTTP. There is currently no frontend or visualization layer. The repo has no tests, no database, and no authentication.

The goal is to add an interactive dashboard for visualizing stock time series data, starting as a personal tool with the option to deploy later.

## Goals / Non-Goals

**Goals:**
- Render candlestick + volume charts from existing `/history` endpoint data
- Support multi-symbol comparison with normalized overlays
- Compute and display technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands)
- Keep the frontend thin — server computes indicators, client renders
- Maintain a clean separation between backend and frontend codebases

**Non-Goals:**
- Real-time/streaming data or WebSocket connections
- User authentication, persistent state, or saved watchlists
- Mobile-optimized or responsive layout
- Drawing tools, annotations, or advanced charting features
- Deployment configuration or CI/CD

## Decisions

### Frontend framework: Vue 3 + Vite + TypeScript

Vue 3 is the user's preferred framework. Vite provides fast HMR and a built-in dev proxy for API requests. TypeScript adds type safety for the chart data structures and API responses.

**Alternatives considered:**
- Streamlit/Dash: Faster to prototype, but limited UI flexibility and harder to deploy as a standalone app later
- React: Viable, but user has more experience with Vue

### Charting library: TradingView Lightweight Charts

Purpose-built for financial data. Candlestick, volume, and line series are first-class primitives. ~40KB gzipped, handles thousands of data points without performance issues.

**Alternatives considered:**
- Apache ECharts: More general-purpose, good candlestick support, but ~300KB and more configuration boilerplate
- Plotly.js: Capable but ~1MB+, can be sluggish with large datasets, less maintained Vue integration

### State management: Vue composables (no store library)

Two composables handle all state: one for API fetching with in-memory caching, one for chart state (symbols, period, indicators). Pinia/Vuex would add complexity without benefit at this scope.

### Indicator computation: Server-side with pandas

Indicators are computed on the backend using pandas operations on the OHLCV DataFrame. This keeps the frontend free of financial math, makes the logic reusable for future consumers (alerts, batch analysis), and avoids shipping computation libraries to the browser.

**Alternatives considered:**
- Client-side computation with a JS library (e.g., technicalindicators): Would eliminate the new endpoint but couples the frontend to indicator logic and increases bundle size

### API design: Separate `/indicators` endpoint

A dedicated endpoint rather than adding indicator data to `/history` responses. This keeps `/history` clean and allows the frontend to fetch OHLCV and indicators in parallel with independent caching.

### Multi-symbol display: Percentage-change normalization

Overlaid symbols use percentage-change from the start of the period rather than absolute prices. This makes comparison meaningful across symbols with vastly different price levels (e.g., AAPL at ~$200 vs BRK-A at ~$600,000).

## Risks / Trade-offs

- **Lightweight Charts sub-pane limitations:** Lightweight Charts doesn't natively support multiple vertically stacked panes with shared time axes. RSI and MACD sub-panes will need to be implemented as separate chart instances with synchronized time scales. → Mitigation: Use the `timeScale().subscribeVisibleTimeRangeChange()` API to sync panes.

- **yfinance rate limiting:** Rapid period/interval changes or many symbols could trigger Yahoo Finance rate limiting. → Mitigation: In-memory caching in the composable prevents redundant fetches. No additional rate limiting needed for a personal tool.

- **Indicator warmup periods:** Indicators like SMA(50) need 50 data points before producing values, leading to gaps at the start of the chart. → Mitigation: Exclude null/NaN values from the API response so the frontend simply receives a shorter series that starts later.

- **No tests initially:** The design prioritizes getting a working dashboard quickly. → Mitigation: The spec scenarios define testable requirements that can be automated later.
