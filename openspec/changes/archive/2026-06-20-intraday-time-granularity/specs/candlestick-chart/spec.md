## MODIFIED Requirements

### Requirement: Candlestick price chart

The dashboard SHALL render OHLCV data as a candlestick chart using TradingView Lightweight Charts. Each candle SHALL represent one data point from the `/history/{symbol}` endpoint. Green candles SHALL indicate close >= open, red candles SHALL indicate close < open. The chart SHALL use Unix epoch seconds (UTCTimestamp) as the time format to support both daily and intraday time precision.

#### Scenario: Candlestick chart renders

- **WHEN** a symbol is added and history data is received
- **THEN** the chart displays candlesticks for the full time range of the data

#### Scenario: Chart is interactive

- **WHEN** a user scrolls or drags on the chart
- **THEN** the chart zooms or pans along the time axis

#### Scenario: Intraday chart renders with sub-day timestamps

- **WHEN** a symbol is added with interval "5m" and period "1d"
- **THEN** the chart displays candlesticks with the time axis showing hours and minutes within the trading day

#### Scenario: Daily chart renders correctly with Unix timestamps

- **WHEN** a symbol is added with interval "1d" and period "1y"
- **THEN** the chart displays daily candlesticks with the time axis showing dates, identical to previous date-string behavior
