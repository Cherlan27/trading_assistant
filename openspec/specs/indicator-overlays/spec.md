# Indicator Overlays

## Purpose

Defines how technical indicators are rendered on the chart, including price pane overlays, RSI and MACD sub-panes, and indicator data caching.

## Requirements

### Requirement: Price pane indicator overlays

SMA, EMA, and Bollinger Bands indicators SHALL render as line series directly on the price pane, overlaid on the candlestick chart. Each indicator SHALL use a distinct color.

#### Scenario: SMA overlay on price chart

- **WHEN** the user enables SMA(20)
- **THEN** a line series representing the 20-period SMA appears on the price pane

#### Scenario: Bollinger Bands overlay

- **WHEN** the user enables Bollinger Bands
- **THEN** three lines (upper, middle, lower) appear on the price pane

### Requirement: RSI sub-pane

RSI SHALL render in its own pane below the volume bars with a separate y-axis scaled from 0 to 100.

#### Scenario: RSI pane appears

- **WHEN** the user enables RSI(14)
- **THEN** a new pane appears below the volume bars showing the RSI line with a 0-100 y-axis

#### Scenario: RSI pane removed

- **WHEN** the user disables RSI(14) and no other sub-pane indicators are active
- **THEN** the RSI pane is removed and the chart layout adjusts

### Requirement: MACD sub-pane

MACD SHALL render in its own pane below the volume bars (or below RSI if both are active) with a separate y-axis. The pane SHALL display the MACD line, signal line, and histogram bars.

#### Scenario: MACD pane appears

- **WHEN** the user enables MACD
- **THEN** a new pane appears showing the MACD line, signal line, and histogram

### Requirement: Indicator data caching

The frontend SHALL cache indicator data in memory keyed by `{symbol}:{period}:{interval}`. When an indicator is toggled off and back on without changing period/interval, the cached data SHALL be used without making an API call.

#### Scenario: Cached indicator toggle

- **WHEN** a user disables SMA(20) and then re-enables it without changing period or interval
- **THEN** the SMA(20) line reappears using cached data without a new API request

#### Scenario: Cache invalidated on period change

- **WHEN** a user changes the period from `1y` to `3mo`
- **THEN** all cached indicator data for the previous period is discarded and new data is fetched
