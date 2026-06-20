## ADDED Requirements

### Requirement: Candlestick price chart

The dashboard SHALL render OHLCV data as a candlestick chart using TradingView Lightweight Charts. Each candle SHALL represent one data point from the `/history/{symbol}` endpoint. Green candles SHALL indicate close >= open, red candles SHALL indicate close < open.

#### Scenario: Candlestick chart renders

- **WHEN** a symbol is added and history data is received
- **THEN** the chart displays candlesticks for the full time range of the data

#### Scenario: Chart is interactive

- **WHEN** a user scrolls or drags on the chart
- **THEN** the chart zooms or pans along the time axis

### Requirement: Volume sub-pane

The dashboard SHALL render a volume bar chart in a pane below the candlestick chart, sharing the same time axis. Volume bars SHALL be color-coded to match their corresponding candlestick (green for up, red for down).

#### Scenario: Volume bars display

- **WHEN** candlestick data is rendered
- **THEN** volume bars appear below the price chart aligned to the same time axis

### Requirement: Crosshair with data display

The chart SHALL display a crosshair that follows the cursor. When the crosshair hovers over a data point, the legend area SHALL display the OHLCV values and any active indicator values for that point in time.

#### Scenario: Hover shows data

- **WHEN** a user moves the cursor over a candlestick
- **THEN** the legend displays the date, open, high, low, close, and volume values for that data point

### Requirement: Color-coded legend

The dashboard SHALL display a legend mapping each symbol and indicator to its line color. The legend SHALL update dynamically as symbols and indicators are added or removed.

#### Scenario: Legend shows active series

- **WHEN** two symbols (AAPL, MSFT) and SMA(20) are active
- **THEN** the legend displays three entries with distinct colors: AAPL, MSFT, and SMA(20)
