## ADDED Requirements

### Requirement: Fetch ticker info by symbol

The system SHALL expose a `GET /info/{symbol}` endpoint that returns company/instrument profile data, financial metrics, and metadata for a given ticker symbol.

#### Scenario: Valid stock symbol

- **WHEN** a client sends `GET /info/AAPL`
- **THEN** the system returns HTTP 200 with a JSON response containing at minimum: `symbol`, `name`, `sector`, `industry`, `market_cap`, `currency`, `exchange`, `description`

#### Scenario: Valid ETF symbol

- **WHEN** a client sends `GET /info/SPY`
- **THEN** the system returns HTTP 200 with available profile data (fields not applicable to ETFs SHALL be `null`)

#### Scenario: Unknown symbol

- **WHEN** a client sends `GET /info/INVALIDXYZ123`
- **THEN** the system returns HTTP 404 with a JSON error body containing a `detail` field

### Requirement: Dividend data included in info response

The info response SHALL include a `dividend_rate` and `dividend_yield` field when available for the instrument. These fields SHALL be `null` for instruments that do not pay dividends.

#### Scenario: Stock with dividends

- **WHEN** a client fetches info for a dividend-paying stock
- **THEN** the response includes non-null `dividend_rate` and `dividend_yield` values

#### Scenario: Instrument without dividends

- **WHEN** a client fetches info for a crypto symbol like `BTC-USD`
- **THEN** the response includes `dividend_rate` and `dividend_yield` as `null`

### Requirement: Info response uses Pydantic model

The info endpoint SHALL return responses validated through a Pydantic model. Fields that vary by instrument type SHALL be typed as `Optional` and default to `None`.

#### Scenario: Response structure is consistent

- **WHEN** a client fetches info for any valid symbol
- **THEN** the response JSON structure matches the documented Pydantic schema with all declared fields present
