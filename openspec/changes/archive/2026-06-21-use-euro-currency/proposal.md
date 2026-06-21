## Why

The dashboard currently displays price values as raw numbers without any currency symbol. Since the tracked instruments are European stocks and ETFs traded in Euro, the UI should clearly indicate Euro (€) as the currency unit to avoid ambiguity.

## What Changes

- Add Euro (€) currency symbol to price displays in the chart legend (Open, High, Low, Close values)
- Add Euro formatting to the chart Y-axis price scale
- Use locale-aware Euro formatting (`de-DE` locale with `EUR` currency) for consistent number formatting (e.g., `1.234,56 €`)

## Capabilities

### New Capabilities

- `euro-currency-display`: Format and display price values with the Euro (€) currency symbol across the dashboard UI

### Modified Capabilities

- `dashboard-app`: Dashboard displays prices with Euro currency formatting instead of raw numbers
- `candlestick-chart`: Chart Y-axis and legend show Euro-formatted prices

## Impact

- **Frontend components**: `ChartLegend.vue`, `PriceChart.vue` — price formatting changes
- **No API changes**: The backend already provides a `currency` field; this change is purely UI-side
- **No breaking changes**: Only visual formatting is affected
