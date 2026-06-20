# FastAPI App

## Purpose

Defines the FastAPI application entrypoint, health check, router-based endpoint organization, upstream error handling, and Poetry-managed dependency configuration.

## Requirements

### Requirement: FastAPI application entrypoint

The system SHALL provide a FastAPI application instance in `yfinance_api/main.py` that can be started with `uvicorn yfinance_api.main:app`. The app SHALL include a title and version in its OpenAPI metadata.

#### Scenario: Application starts successfully

- **WHEN** a user runs `uvicorn yfinance_api.main:app`
- **THEN** the server starts and accepts HTTP requests on the default port

#### Scenario: OpenAPI docs available

- **WHEN** a client navigates to `/docs`
- **THEN** the system serves the Swagger UI with all endpoints documented

### Requirement: Health check endpoint

The system SHALL expose a `GET /health` endpoint that returns the service status without requiring any external dependencies.

#### Scenario: Health check returns OK

- **WHEN** a client sends `GET /health`
- **THEN** the system returns HTTP 200 with `{"status": "ok"}`

### Requirement: Router-based endpoint organization

The application SHALL organize endpoints into separate FastAPI router modules: one for quote, one for history, one for info, and one for indicators. Each router SHALL be registered with the main app via `app.include_router()`.

#### Scenario: Routers are registered

- **WHEN** the application starts
- **THEN** all routes from the quote, history, info, and indicators routers are accessible

### Requirement: Upstream error handling

The application SHALL catch exceptions from the yfinance service layer and return appropriate HTTP error responses. Network failures communicating with Yahoo Finance SHALL result in HTTP 502 responses.

#### Scenario: Yahoo Finance unreachable

- **WHEN** a client requests any data endpoint and yfinance fails to connect to Yahoo Finance
- **THEN** the system returns HTTP 502 with a `detail` field explaining the upstream service is unavailable

### Requirement: CORS middleware

The application SHALL include CORS middleware allowing requests from the Vite dev server origin (`http://localhost:5173`). The middleware SHALL allow all HTTP methods and headers needed for API consumption.

#### Scenario: Cross-origin request allowed

- **WHEN** the Vite dev server at `http://localhost:5173` makes a request to the API
- **THEN** the response includes appropriate CORS headers and the request succeeds

#### Scenario: Preflight request handled

- **WHEN** the browser sends an OPTIONS preflight request from `http://localhost:5173`
- **THEN** the server responds with HTTP 200 and the correct CORS headers

### Requirement: Poetry-managed dependencies

The project SHALL use Poetry for dependency management with a `pyproject.toml` at the repository root. The pyproject.toml SHALL declare: `fastapi`, `uvicorn[standard]`, `yfinance`, and `pydantic` as dependencies, with Python `>=3.11` required.

#### Scenario: Dependencies installable via Poetry

- **WHEN** a user runs `poetry install` in the project root
- **THEN** all dependencies are installed and the application can be started
