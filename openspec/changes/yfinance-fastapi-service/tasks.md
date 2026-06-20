## 1. Project Scaffolding

- [x] 1.1 Create `pyproject.toml` with Poetry configuration, Python >=3.11, and dependencies: fastapi, uvicorn[standard], yfinance, pydantic
- [x] 1.2 Create package directory structure: `yfinance_api/` with `__init__.py`, `main.py`, and subdirectories `routers/`, `schemas/`, `services/` (each with `__init__.py`)
- [x] 1.3 Run `poetry install` to generate lock file and verify dependencies resolve

## 2. Pydantic Response Models

- [x] 2.1 Create `yfinance_api/schemas/quote.py` with `QuoteResponse` model (symbol, price, currency, exchange, market_state, previous_close, open, day_high, day_low, volume, market_cap — optional fields as `Optional`)
- [x] 2.2 Create `yfinance_api/schemas/history.py` with `OHLCVDataPoint` model (date, open, high, low, close, volume) and `HistoryResponse` model (symbol, data: list of data points)
- [x] 2.3 Create `yfinance_api/schemas/info.py` with `TickerInfoResponse` model (symbol, name, sector, industry, market_cap, currency, exchange, description, dividend_rate, dividend_yield — optional fields as `Optional`)

## 3. YFinance Service Layer

- [x] 3.1 Create `yfinance_api/services/yfinance_service.py` with `YFinanceService` class
- [x] 3.2 Implement `get_quote(symbol)` method — fetch quote data via `yfinance.Ticker`, detect invalid symbols (empty/None results → raise HTTPException 404), convert to `QuoteResponse`
- [x] 3.3 Implement `get_history(symbol, period, interval)` method — fetch OHLCV via `ticker.history()`, detect empty DataFrame → raise HTTPException 404, convert rows to `HistoryResponse`
- [x] 3.4 Implement `get_info(symbol)` method — fetch info dict via `ticker.info`, detect invalid symbols → raise HTTPException 404, convert to `TickerInfoResponse`
- [x] 3.5 Add network error handling — catch connection/request exceptions from yfinance and raise HTTPException 502 with upstream failure detail

## 4. FastAPI Routers

- [x] 4.1 Create `yfinance_api/routers/quote.py` with `GET /quote/{symbol}` endpoint using `YFinanceService.get_quote()`
- [x] 4.2 Create `yfinance_api/routers/history.py` with `GET /history/{symbol}` endpoint, `period` query param (Literal enum, default `1mo`), `interval` query param (Literal enum, default `1d`)
- [x] 4.3 Create `yfinance_api/routers/info.py` with `GET /info/{symbol}` endpoint using `YFinanceService.get_info()`

## 5. Application Entrypoint

- [x] 5.1 Create `yfinance_api/main.py` with FastAPI app instance (title, version), `GET /health` endpoint returning `{"status": "ok"}`
- [x] 5.2 Register all three routers via `app.include_router()` for quote, history, and info

## 6. Smoke Test

- [x] 6.1 Start the server with `uvicorn yfinance_api.main:app` and verify `/health` returns 200
- [x] 6.2 Verify `/docs` serves Swagger UI with all endpoints listed
- [x] 6.3 Test `GET /quote/AAPL`, `GET /history/AAPL`, and `GET /info/AAPL` return valid JSON responses
- [x] 6.4 Test `GET /quote/INVALIDXYZ123` returns 404
