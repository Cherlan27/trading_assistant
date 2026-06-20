# Multi-Symbol Comparison

## Purpose

Defines how multiple ticker symbols are displayed simultaneously on the chart, including overlay rendering, percentage-change normalization, and independent data fetching.

## Requirements

### Requirement: Multi-symbol overlay

When multiple symbols are loaded, the dashboard SHALL display the first symbol as a candlestick chart and overlay additional symbols as line series on the same price pane.

#### Scenario: Second symbol added

- **WHEN** a user adds "MSFT" while "AAPL" is already displayed
- **THEN** MSFT appears as a line series overlaid on the AAPL candlestick chart with a distinct color

#### Scenario: Symbol removed from multi-view

- **WHEN** a user removes one of the overlaid symbols
- **THEN** that symbol's line series is removed and the remaining chart data stays intact

### Requirement: Percentage-change normalization for comparison

Since different symbols have different absolute price levels, overlaid symbols SHALL be displayed using percentage-change normalization from the start of the visible period. The y-axis for overlaid line series SHALL show percentage change, not absolute price.

#### Scenario: Normalized comparison

- **WHEN** AAPL (price ~$200) and BRK-A (price ~$600,000) are both loaded
- **THEN** both are displayed as percentage change from their starting price, making visual comparison meaningful

### Requirement: Independent data fetching per symbol

Each symbol SHALL fetch its own history and indicator data independently. A failure to load one symbol SHALL NOT prevent other symbols from displaying.

#### Scenario: One symbol fails

- **WHEN** a user adds an invalid symbol while a valid symbol is displayed
- **THEN** the invalid symbol shows an error toast and the valid symbol's chart remains unaffected
