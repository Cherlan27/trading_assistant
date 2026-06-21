# Euro Currency Display

## Purpose

Defines the Euro currency formatting behavior for price values across the trading dashboard, ensuring consistent German locale formatting.

## Requirements

### Requirement: Euro price formatting

The dashboard SHALL format all price values (Open, High, Low, Close) using the Euro currency format with German locale (`de-DE`). Prices SHALL display with the Euro symbol (€), dot as thousands separator, and comma as decimal separator (e.g., `1.234,56 €`). A shared `formatPrice` utility function SHALL be used for consistent formatting across all components.

#### Scenario: Price values display with Euro symbol in legend

- **WHEN** the crosshair hovers over a candlestick data point
- **THEN** the legend displays OHLC values formatted as Euro amounts (e.g., `O: 1.234,56 € H: 1.240,00 € L: 1.230,00 € C: 1.238,50 €`)

#### Scenario: Small price values display with Euro symbol

- **WHEN** the crosshair hovers over a data point with a price below 1.000
- **THEN** the legend displays the price formatted as Euro without thousands separator (e.g., `O: 45,20 €`)

#### Scenario: Chart Y-axis shows Euro-formatted prices

- **WHEN** a symbol is loaded and the candlestick chart renders
- **THEN** the right-side price scale labels display prices with the Euro symbol and German locale formatting

### Requirement: Volume formatting remains unchanged

Volume values SHALL NOT display a currency symbol. Volume SHALL continue to use abbreviated formatting (K, M, B suffixes).

#### Scenario: Volume displays without currency symbol

- **WHEN** the crosshair hovers over a candlestick data point
- **THEN** the volume value displays with abbreviated formatting (e.g., `V: 1.5M`) without any currency symbol
