# Historical Data

## Purpose

Defines the historical OHLCV data endpoint, including configurable period and interval parameters, response structure, and error handling.

## Requirements

### Requirement: Fetch historical OHLCV data by symbol

The system SHALL expose a `GET /history/{symbol}` endpoint that returns historical OHLCV (open, high, low, close, volume) time series data for a given ticker symbol.

#### Scenario: Default parameters

- **WHEN** a client sends `GET /history/AAPL` with no query parameters
- **THEN** the system returns HTTP 200 with OHLCV data for the last 1 month at daily intervals

#### Scenario: Custom period and interval

- **WHEN** a client sends `GET /history/AAPL?period=1y&interval=1wk`
- **THEN** the system returns HTTP 200 with weekly OHLCV data for the last year

#### Scenario: Unknown symbol

- **WHEN** a client sends `GET /history/INVALIDXYZ123`
- **THEN** the system returns HTTP 404 with a JSON error body containing a `detail` field

### Requirement: Configurable period parameter

The endpoint SHALL accept a `period` query parameter with valid values: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`. The default SHALL be `1mo`.

#### Scenario: Invalid period value

- **WHEN** a client sends `GET /history/AAPL?period=abc`
- **THEN** the system returns HTTP 422 with a validation error indicating the allowed period values

### Requirement: Configurable interval parameter

The endpoint SHALL accept an `interval` query parameter with valid values: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`. The default SHALL be `1d`.

#### Scenario: Invalid interval value

- **WHEN** a client sends `GET /history/AAPL?interval=2d`
- **THEN** the system returns HTTP 422 with a validation error indicating the allowed interval values

### Requirement: History response structure

Each data point in the response SHALL contain: `date` (ISO 8601 string), `open`, `high`, `low`, `close`, and `volume`. The response SHALL include a `symbol` field and a `data` array of these data points.

#### Scenario: Response contains OHLCV array

- **WHEN** a client sends `GET /history/MSFT?period=5d&interval=1d`
- **THEN** the response contains a `symbol` field set to `"MSFT"` and a `data` array where each element has `date`, `open`, `high`, `low`, `close`, and `volume` fields
