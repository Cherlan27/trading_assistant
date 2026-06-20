## MODIFIED Requirements

### Requirement: Router-based endpoint organization

The application SHALL organize endpoints into separate FastAPI router modules: one for quote, one for history, one for info, and one for indicators. Each router SHALL be registered with the main app via `app.include_router()`.

#### Scenario: Routers are registered

- **WHEN** the application starts
- **THEN** all routes from the quote, history, info, and indicators routers are accessible

## ADDED Requirements

### Requirement: CORS middleware

The application SHALL include CORS middleware allowing requests from the Vite dev server origin (`http://localhost:5173`). The middleware SHALL allow all HTTP methods and headers needed for API consumption.

#### Scenario: Cross-origin request allowed

- **WHEN** the Vite dev server at `http://localhost:5173` makes a request to the API
- **THEN** the response includes appropriate CORS headers and the request succeeds

#### Scenario: Preflight request handled

- **WHEN** the browser sends an OPTIONS preflight request from `http://localhost:5173`
- **THEN** the server responds with HTTP 200 and the correct CORS headers
