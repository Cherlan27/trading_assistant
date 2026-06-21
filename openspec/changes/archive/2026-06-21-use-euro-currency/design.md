## Context

The dashboard displays price values (OHLC) as raw numbers without any currency symbol. The `ChartLegend.vue` component uses a `formatNum` function that applies `toLocaleString` or `toFixed(2)` without currency context. The `PriceChart.vue` candlestick series uses the lightweight-charts default price format (no currency symbol). The backend already provides a `currency` field in quote/info responses, but the frontend ignores it.

## Goals / Non-Goals

**Goals:**
- Display Euro (€) currency symbol alongside price values in the chart legend (OHLC values)
- Format the chart Y-axis price labels with the Euro symbol
- Use German locale (`de-DE`) for number formatting (dot as thousands separator, comma as decimal separator, e.g., `1.234,56 €`)

**Non-Goals:**
- Dynamic currency switching based on the symbol's native currency (hardcode Euro for now)
- Currency conversion (prices remain as provided by the API)
- Changing volume formatting (volume stays as abbreviated numbers without currency)
- Modifying the API or backend

## Decisions

### 1. Centralized formatting utility

**Decision**: Create a `formatPrice` function in `constants.ts` (or a small utility) that uses `Intl.NumberFormat` with `de-DE` locale and `EUR` currency.

**Rationale**: `Intl.NumberFormat` is browser-native, handles locale-specific grouping/decimal separators, and avoids manual string building. Centralizing it avoids duplication between ChartLegend and PriceChart.

**Alternative considered**: Passing a currency prop from parent components — adds complexity without benefit since we're hardcoding Euro.

### 2. Lightweight Charts custom price formatter

**Decision**: Apply a `priceFormat` with `type: 'custom'` and a `formatter` callback on the candlestick series to display Euro-formatted prices on the Y-axis.

**Rationale**: Lightweight Charts supports custom formatters natively. This ensures the right-side price scale shows `1.234,56 €` instead of plain numbers.

### 3. Legend formatting

**Decision**: Replace `formatNum` in `ChartLegend.vue` with the shared `formatPrice` function for OHLC values. Keep `formatVolume` unchanged (volume is not a currency value).

**Rationale**: OHLC values represent prices in Euro; volume represents share count. Different formatting is appropriate.

## Risks / Trade-offs

- **Hardcoded locale**: Using `de-DE` locale means the formatting won't adapt if a user prefers a different locale. → Acceptable for now; the dashboard targets German-speaking users.
- **Non-Euro instruments**: If a user queries a USD-denominated symbol, it will still show €. → Accepted as non-goal; dynamic currency switching can be added later.
- **Y-axis width**: Euro-formatted prices with symbol are wider than plain numbers. → Lightweight Charts adjusts the price scale width automatically.
