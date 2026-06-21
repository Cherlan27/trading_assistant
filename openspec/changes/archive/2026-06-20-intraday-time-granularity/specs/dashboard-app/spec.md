## MODIFIED Requirements

### Requirement: Interval selector

The controls SHALL include a dropdown for selecting the data interval. Valid values SHALL be: `1m`, `5m`, `15m`, `30m`, `1h`, `1d`, `1wk`, `1mo`. The default SHALL be `1d`. The available intervals SHALL be filtered based on the selected period to prevent invalid combinations using a static compatibility map.

#### Scenario: Change interval

- **WHEN** a user selects "1wk" from the interval dropdown
- **THEN** the chart re-fetches and displays weekly data for all loaded symbols

#### Scenario: Intraday interval selected

- **WHEN** a user selects period "1d" and interval "5m"
- **THEN** the chart re-fetches and displays 5-minute candles for the current day for all loaded symbols

#### Scenario: Invalid interval filtered out

- **WHEN** a user selects period "1y"
- **THEN** the interval dropdown SHALL only show `1d`, `1wk`, `1mo` and SHALL NOT show intraday intervals

#### Scenario: Interval auto-adjusted on period change

- **WHEN** a user has interval "5m" selected and changes period from "1d" to "1y"
- **THEN** the interval SHALL auto-adjust to the first valid interval for the new period (e.g., `1d`)
