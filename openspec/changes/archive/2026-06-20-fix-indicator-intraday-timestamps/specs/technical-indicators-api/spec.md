## MODIFIED Requirements

### Requirement: Period and interval parameters

The endpoint SHALL accept `period` and `interval` query parameters matching the same values as the `/history/{symbol}` endpoint. These parameters SHALL control the OHLCV data range used for indicator computation. The `date` field in all indicator response data points SHALL use ISO-8601 format (`isoformat()`), preserving the full datetime including time component for intraday intervals. This format SHALL match the `date` field format used by the `/history/{symbol}` endpoint.

#### Scenario: Custom period

- **WHEN** a client sends `GET /indicators/AAPL?period=3mo&interval=1d&indicators=sma_20`
- **THEN** the indicators are computed from 3 months of daily OHLCV data

#### Scenario: Intraday interval date format

- **WHEN** a client sends `GET /indicators/AAPL?period=1d&interval=5m&indicators=sma_20`
- **THEN** each data point's `date` field contains a full ISO-8601 datetime string with time component (e.g., `2024-01-15T10:30:00+00:00`)
- **AND** the `date` format matches the format returned by `GET /history/AAPL?period=1d&interval=5m`

#### Scenario: Daily interval date format

- **WHEN** a client sends `GET /indicators/AAPL?period=1y&interval=1d&indicators=sma_20`
- **THEN** each data point's `date` field contains a full ISO-8601 datetime string (e.g., `2024-01-15T00:00:00+00:00`)
