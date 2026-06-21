## MODIFIED Requirements

### Requirement: Candlestick price chart

The dashboard SHALL render OHLCV data as a candlestick chart using TradingView Lightweight Charts. Each candle SHALL represent one data point from the `/history/{symbol}` endpoint. Green candles SHALL indicate close >= open, red candles SHALL indicate close < open. The chart SHALL use Unix epoch seconds (UTCTimestamp) as the time format to support both daily and intraday time precision. The chart SHALL dynamically toggle time visibility on the x-axis based on the active interval: `timeVisible` SHALL be `true` for intraday intervals (1m, 5m, 15m, 30m, 1h) and `false` for daily or longer intervals (1d, 1wk, 1mo). The right-side price scale SHALL display prices using a custom formatter with Euro currency formatting and German locale (e.g., `1.234,56 €`).

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
- **THEN** the chart displays daily candlesticks with the time axis showing dates only, without hours or minutes

#### Scenario: Time visibility toggles on interval change

- **WHEN** a user switches from interval "1d" to interval "5m"
- **THEN** the x-axis updates to show hours and minutes without requiring a page reload or chart recreation

#### Scenario: Time visibility toggles back to date-only

- **WHEN** a user switches from interval "5m" to interval "1d"
- **THEN** the x-axis updates to show dates only, hiding hours and minutes

#### Scenario: Y-axis displays Euro-formatted prices

- **WHEN** a symbol is loaded and the candlestick chart renders
- **THEN** the right-side price scale labels show prices formatted with the Euro symbol and German locale (e.g., `1.234,56 €`)

### Requirement: Crosshair with data display

The chart SHALL display a crosshair that follows the cursor. When the crosshair hovers over a data point, the legend area SHALL display the OHLCV values formatted with Euro currency and any active indicator values for that point in time.

#### Scenario: Hover shows data

- **WHEN** a user moves the cursor over a candlestick
- **THEN** the legend displays the date, open, high, low, close values in Euro format, and volume for that data point
