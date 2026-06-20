## Context

This is a greenfield Python package within the `trading_trend` project. There is no existing application code — only project scaffolding and openspec planning infrastructure. The package will be the first runnable service in this repository, providing financial market data via a REST API backed by Yahoo Finance through the yfinance library.

## Goals / Non-Goals

**Goals:**
- Provide a clean REST API for retrieving stock quotes, historical OHLCV data, and ticker info
- Use Poetry for dependency management with a well-structured `pyproject.toml`
- Return structured, typed JSON responses via Pydantic models
- Support any yfinance-compatible symbol: stocks, ETFs, indices, mutual funds, currencies (e.g., `EURUSD=X`), crypto (e.g., `BTC-USD`)
- Keep the service simple and stateless — no database, no auth, no caching layer

**Non-Goals:**
- Real-time streaming / WebSocket support
- User authentication or API key management
- Persistent storage or caching of financial data
- Rate limiting or request throttling
- Frontend / UI of any kind
- Webhook or event-driven notifications

## Decisions

### 1. Package structure: flat source layout

Use a flat `yfinance_api/` package directory at the repo root with a `pyproject.toml` alongside it.

```
trading_trend/
├── pyproject.toml
├── yfinance_api/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entrypoint
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── quote.py     # /quote endpoints
│   │   ├── history.py   # /history endpoints
│   │   └── info.py      # /info endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── quote.py     # Quote response models
│   │   ├── history.py   # OHLCV response models
│   │   └── info.py      # Ticker info response models
│   └── services/
│       ├── __init__.py
│       └── yfinance_service.py  # yfinance wrapper
```

**Why over `src/` layout:** This is a standalone service, not a distributable library. A flat layout keeps imports simple (`from yfinance_api.routers import quote`) and aligns with FastAPI conventions.

### 2. yfinance access: thin service wrapper

Wrap yfinance calls in a `YFinanceService` class rather than calling `yfinance.Ticker()` directly in route handlers.

**Why:** Isolates yfinance's untyped return values (dicts, DataFrames) from the API layer. The service converts raw yfinance output into Pydantic models, keeping routers thin.

**Alternative considered:** Direct yfinance calls in handlers — rejected because it mixes data transformation with request handling and makes testing harder.

### 3. API design: resource-oriented routes

```
GET /quote/{symbol}           → current price/quote
GET /history/{symbol}         → OHLCV time series
GET /info/{symbol}            → company profile, financials, metadata
GET /health                   → service health check
```

Query parameters for `/history`:
- `period` (default: `1mo`) — yfinance period string (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- `interval` (default: `1d`) — yfinance interval string (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

**Why over nested resources (e.g., `/ticker/{symbol}/quote`):** Flat routes are simpler for this scope. Each endpoint maps 1:1 to a distinct yfinance operation, and there's no shared state between them that would benefit from nesting.

### 4. Error handling: map yfinance failures to HTTP errors

yfinance does not raise clean exceptions — it often returns empty DataFrames or None for invalid symbols. The service layer will detect these cases and raise FastAPI `HTTPException` with appropriate status codes:

- Invalid/unknown symbol → 404
- yfinance network error → 502 (bad gateway, upstream failure)
- Invalid query parameters → 422 (handled by FastAPI/Pydantic validation)

### 5. Python version and dependencies

- Python 3.11+ (for modern typing features like `str | None`)
- FastAPI + uvicorn[standard] for the web server
- yfinance for data retrieval
- pydantic v2 (bundled with FastAPI)

Poetry manages all dependencies via `pyproject.toml`. No extras or optional dependency groups for now.

## Risks / Trade-offs

- **Yahoo Finance reliability** → yfinance scrapes Yahoo Finance, which can change its API without notice. Mitigation: the service wrapper isolates this; if yfinance breaks, only `yfinance_service.py` needs updating.
- **Rate limiting by Yahoo** → Heavy usage may trigger Yahoo's rate limits, returning errors or stale data. Mitigation: not addressed in v1 (non-goal), but the service layer is the natural place to add throttling later.
- **Untyped yfinance output** → yfinance returns dicts and DataFrames with inconsistent keys depending on the ticker type. Mitigation: Pydantic models with `Optional` fields and defensive parsing in the service layer.
- **No tests in v1** → Initial implementation ships without a test suite. Mitigation: the service/router separation makes it straightforward to add tests later with a mocked service layer.
