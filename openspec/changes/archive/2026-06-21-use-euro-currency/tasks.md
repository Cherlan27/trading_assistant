## 1. Price Formatting Utility

- [x] 1.1 Add `formatPrice` function to `dashboard/src/constants.ts` using `Intl.NumberFormat` with `de-DE` locale and `EUR` currency style

## 2. Chart Legend

- [x] 2.1 Import `formatPrice` in `ChartLegend.vue` and replace `formatNum` usage for OHLC values with `formatPrice`
- [x] 2.2 Keep `formatVolume` unchanged for volume display

## 3. Chart Y-Axis

- [x] 3.1 Add custom `priceFormat` with `type: 'custom'` and Euro formatter callback to the candlestick series in `PriceChart.vue`

## 4. Verification

- [x] 4.1 Start dev server and verify Euro formatting on legend OHLC values and chart Y-axis
