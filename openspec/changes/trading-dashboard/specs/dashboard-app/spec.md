## ADDED Requirements

### Requirement: Vue 3 application scaffolding

The dashboard SHALL be a Vue 3 + TypeScript application built with Vite, located in the `dashboard/` directory at the repository root. The application SHALL be a single-page app with no client-side routing.

#### Scenario: Development server starts

- **WHEN** a developer runs `npm run dev` in the `dashboard/` directory
- **THEN** the Vite dev server starts and serves the application on port 5173

#### Scenario: Production build

- **WHEN** a developer runs `npm run build` in the `dashboard/` directory
- **THEN** Vite produces a production bundle in `dashboard/dist/`

### Requirement: API proxy in development

The Vite dev server SHALL proxy API requests to the FastAPI backend at `http://localhost:8000`. All requests matching `/api/*` or direct API paths (`/history/*`, `/quote/*`, `/info/*`, `/indicators/*`, `/health`) SHALL be forwarded to the backend.

#### Scenario: API call proxied to backend

- **WHEN** the frontend makes a request to `/history/AAPL` during development
- **THEN** the Vite dev server forwards the request to `http://localhost:8000/history/AAPL` and returns the response

### Requirement: Dashboard layout with controls and chart area

The application SHALL render a single-page layout with three zones: a top bar containing controls (symbol input, period/interval selectors, indicator toggles), a main area for the chart, and a bottom legend area.

#### Scenario: Initial page load

- **WHEN** a user opens the dashboard in a browser
- **THEN** the page displays the control bar, an empty chart area, and the legend section

### Requirement: Symbol input with chip management

The controls SHALL include a text input for entering ticker symbols. When the user submits a symbol, it SHALL appear as a removable chip/tag. Multiple symbols SHALL be supported simultaneously.

#### Scenario: Add a symbol

- **WHEN** a user types "AAPL" and presses Enter
- **THEN** the symbol "AAPL" appears as a chip and chart data loads for that symbol

#### Scenario: Remove a symbol

- **WHEN** a user clicks the remove button on a symbol chip
- **THEN** the chip is removed and the symbol's data is removed from the chart

### Requirement: Period selector

The controls SHALL include a dropdown for selecting the data period. Valid values SHALL be: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `max`. The default SHALL be `1y`.

#### Scenario: Change period

- **WHEN** a user selects "3mo" from the period dropdown
- **THEN** the chart re-fetches and displays data for the last 3 months for all loaded symbols

### Requirement: Interval selector

The controls SHALL include a dropdown for selecting the data interval. Valid values SHALL be: `1d`, `1wk`, `1mo`. The default SHALL be `1d`. The available intervals SHALL be filtered based on the selected period to prevent invalid combinations.

#### Scenario: Change interval

- **WHEN** a user selects "1wk" from the interval dropdown
- **THEN** the chart re-fetches and displays weekly data for all loaded symbols

### Requirement: Indicator toggles

The controls SHALL include toggle buttons for technical indicators: SMA(20), SMA(50), EMA(20), RSI(14), MACD, Bollinger Bands(20,2). Each toggle SHALL independently enable or disable its indicator on the chart.

#### Scenario: Enable an indicator

- **WHEN** a user toggles SMA(20) on
- **THEN** the SMA(20) line appears on the price chart for all loaded symbols

#### Scenario: Disable an indicator

- **WHEN** a user toggles SMA(20) off
- **THEN** the SMA(20) line is removed from the chart without an API call
