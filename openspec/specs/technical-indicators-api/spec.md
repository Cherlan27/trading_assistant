# Technical Indicators API

## Purpose

Defines the backend API endpoint for computing and returning technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands) from OHLCV data.

## Requirements

### Requirement: Technical indicators endpoint

The system SHALL expose a `GET /indicators/{symbol}` endpoint that computes and returns technical indicators from OHLCV data for a given ticker symbol.

#### Scenario: Fetch SMA indicator

- **WHEN** a client sends `GET /indicators/AAPL?period=1y&interval=1d&indicators=sma_20`
- **THEN** the system returns HTTP 200 with a JSON object containing `sma_20` as an array of `{date, value}` data points

#### Scenario: Fetch multiple indicators

- **WHEN** a client sends `GET /indicators/AAPL?period=1y&interval=1d&indicators=sma_20,rsi_14,macd`
- **THEN** the system returns HTTP 200 with a JSON object containing keys `sma_20`, `rsi_14`, and `macd`, each with their respective data point arrays

#### Scenario: Unknown symbol

- **WHEN** a client sends `GET /indicators/INVALIDXYZ123?indicators=sma_20`
- **THEN** the system returns HTTP 404 with a JSON error body containing a `detail` field

### Requirement: Indicator query parameter format

The `indicators` query parameter SHALL accept a comma-separated list of indicator identifiers. Each identifier SHALL follow the pattern `{type}_{param}` (e.g., `sma_20`, `ema_50`, `rsi_14`, `bbands_20`) except `macd` which SHALL use fixed standard parameters (12, 26, 9). If `indicators` is omitted, the endpoint SHALL return an empty object.

#### Scenario: No indicators requested

- **WHEN** a client sends `GET /indicators/AAPL?period=1y&interval=1d` without an `indicators` parameter
- **THEN** the system returns HTTP 200 with an empty JSON object `{}`

#### Scenario: Invalid indicator name

- **WHEN** a client sends `GET /indicators/AAPL?indicators=invalid_foo`
- **THEN** the system returns HTTP 422 with a validation error

### Requirement: SMA and EMA computation

The endpoint SHALL compute Simple Moving Average (SMA) and Exponential Moving Average (EMA) using the close price. The window size SHALL be specified in the indicator identifier (e.g., `sma_20` = 20-period SMA). Response format: `[{date, value}, ...]`.

#### Scenario: SMA values

- **WHEN** a client requests `sma_20`
- **THEN** each data point contains the 20-period simple moving average of the close price, with `null` values excluded for the initial warmup period

### Requirement: RSI computation

The endpoint SHALL compute Relative Strength Index using the standard gain/loss rolling calculation. The period SHALL be specified in the identifier (e.g., `rsi_14` = 14-period RSI). Response format: `[{date, value}, ...]`.

#### Scenario: RSI values

- **WHEN** a client requests `rsi_14`
- **THEN** each data point contains the 14-period RSI value between 0 and 100

### Requirement: MACD computation

The endpoint SHALL compute Moving Average Convergence Divergence using fixed parameters: EMA(12), EMA(26), signal line = EMA(9) of MACD. Response format: `[{date, macd, signal, histogram}, ...]`.

#### Scenario: MACD values

- **WHEN** a client requests `macd`
- **THEN** each data point contains `macd` (EMA12 - EMA26), `signal` (EMA9 of MACD), and `histogram` (MACD - signal)

### Requirement: Bollinger Bands computation

The endpoint SHALL compute Bollinger Bands using SMA and rolling standard deviation. The window SHALL be specified in the identifier (e.g., `bbands_20` = 20-period, 2 standard deviations). Response format: `[{date, upper, middle, lower}, ...]`.

#### Scenario: Bollinger Bands values

- **WHEN** a client requests `bbands_20`
- **THEN** each data point contains `upper` (SMA + 2*std), `middle` (SMA), and `lower` (SMA - 2*std)

### Requirement: Period and interval parameters

The endpoint SHALL accept `period` and `interval` query parameters matching the same values as the `/history/{symbol}` endpoint. These parameters SHALL control the OHLCV data range used for indicator computation.

#### Scenario: Custom period

- **WHEN** a client sends `GET /indicators/AAPL?period=3mo&interval=1d&indicators=sma_20`
- **THEN** the indicators are computed from 3 months of daily OHLCV data
