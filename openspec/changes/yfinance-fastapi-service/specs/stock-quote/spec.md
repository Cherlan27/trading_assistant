## ADDED Requirements

### Requirement: Fetch current quote by symbol

The system SHALL expose a `GET /quote/{symbol}` endpoint that returns the current price and quote data for a given ticker symbol. The symbol parameter SHALL accept any yfinance-compatible identifier including stocks (e.g., `AAPL`), ETFs (e.g., `SPY`), indices (e.g., `^GSPC`), currencies (e.g., `EURUSD=X`), and crypto (e.g., `BTC-USD`).

#### Scenario: Valid stock symbol

- **WHEN** a client sends `GET /quote/AAPL`
- **THEN** the system returns HTTP 200 with a JSON response containing at minimum: `symbol`, `price`, `currency`, `exchange`, `market_state`, `previous_close`, `open`, `day_high`, `day_low`, `volume`

#### Scenario: Valid crypto symbol

- **WHEN** a client sends `GET /quote/BTC-USD`
- **THEN** the system returns HTTP 200 with a JSON response containing quote data for Bitcoin in USD

#### Scenario: Unknown symbol

- **WHEN** a client sends `GET /quote/INVALIDXYZ123`
- **THEN** the system returns HTTP 404 with a JSON error body containing a `detail` field explaining the symbol was not found

### Requirement: Quote response uses Pydantic model

The quote endpoint SHALL return responses validated through a Pydantic model. Fields that may not be available for all instrument types (e.g., `market_cap` for currencies) SHALL be typed as `Optional` and default to `None`.

#### Scenario: Response structure is consistent

- **WHEN** a client fetches a quote for any valid symbol
- **THEN** the response JSON structure matches the documented Pydantic schema with all declared fields present (nullable fields included as `null`)
