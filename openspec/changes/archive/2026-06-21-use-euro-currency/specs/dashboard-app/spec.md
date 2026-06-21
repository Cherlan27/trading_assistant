## MODIFIED Requirements

### Requirement: Dashboard layout with controls and chart area

The application SHALL render a single-page layout with three zones: a top bar containing controls (symbol input, period/interval selectors, indicator toggles), a main area for the chart, and a bottom legend area. All price values displayed in the legend SHALL use Euro currency formatting with German locale.

#### Scenario: Initial page load

- **WHEN** a user opens the dashboard in a browser
- **THEN** the page displays the control bar, an empty chart area, and the legend section

#### Scenario: Legend shows Euro-formatted prices

- **WHEN** a user hovers over chart data
- **THEN** the legend area displays OHLC values with Euro currency formatting (e.g., `1.234,56 €`)
