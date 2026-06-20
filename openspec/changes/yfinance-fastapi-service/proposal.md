## Why

The trading_trend project needs a programmatic way to retrieve financial market data. A Python package with a FastAPI REST API backed by yfinance provides a self-hosted service for fetching stock quotes, historical price data, and financial information — decoupling data retrieval from any specific UI or analysis tool.

## What Changes

- New Python package scaffolded with Poetry and `pyproject.toml` for dependency management
- FastAPI application exposing REST endpoints for financial data retrieval
- yfinance integration for fetching data by ticker symbol (stocks, ETFs, indices, mutual funds, currencies, crypto)
- Endpoints for: current quote/price, historical OHLCV time series, and ticker financial info (company profile, financials, dividends)
- Pydantic response models for structured, typed API responses

## Capabilities

### New Capabilities

- `stock-quote`: Fetch current price and quote data for a given ticker symbol
- `historical-data`: Retrieve historical OHLCV (open, high, low, close, volume) time series with configurable period and interval
- `ticker-info`: Get company/instrument profile, financial metrics, dividends, and metadata for a ticker
- `fastapi-app`: The FastAPI application shell — routing, configuration, error handling, and app entrypoint

### Modified Capabilities

_None — this is a new package with no existing capabilities._

## Impact

- **Dependencies**: Python 3.11+, FastAPI, uvicorn, yfinance, pydantic (managed via Poetry)
- **Project structure**: New package directory at the project root (e.g., `yfinance_api/`) with `pyproject.toml`
- **APIs**: New HTTP REST endpoints under the service
- **Systems**: Relies on Yahoo Finance as the upstream data source (rate limits and availability apply)
