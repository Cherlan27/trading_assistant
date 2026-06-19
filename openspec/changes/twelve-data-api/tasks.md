## 1. Projekt-Setup

- [ ] 1.1 `pyproject.toml` erstellen mit Abhängigkeiten (fastapi, uvicorn, httpx, pydantic-settings, python-dotenv)
- [ ] 1.2 Verzeichnisstruktur anlegen: `app/`, `app/routers/`, `app/schemas/`, `app/services/` mit `__init__.py`-Dateien
- [ ] 1.3 `.env.example` erstellen mit `TWELVE_DATA_API_KEY=your-api-key-here`
- [ ] 1.4 `app/config.py` implementieren: Settings-Klasse mit `TWELVE_DATA_API_KEY` und `TWELVE_DATA_BASE_URL` via pydantic-settings

## 2. Twelve Data Client

- [ ] 2.1 `app/services/twelve_data.py` implementieren: Async HTTP-Client mit httpx, API-Key als Query-Parameter, Base-URL-Konfiguration
- [ ] 2.2 Fehlerbehandlung einbauen: Twelve Data Error-Responses erkennen (`status: "error"`), Timeout (10s), Rate-Limit (429) weiterleiten

## 3. Schemas

- [ ] 3.1 `app/schemas/time_series.py` implementieren: Query-Parameter-Schema (symbol, interval, start_date, end_date) und Response-Modell (OHLCV-Datenpunkte)
- [ ] 3.2 `app/schemas/quote.py` implementieren: Query-Parameter-Schema (symbol) und Response-Modell (Kurs, Name, Börse, Timestamp)
- [ ] 3.3 `app/schemas/indicators.py` implementieren: Query-Parameter-Schema (symbol, interval, time_period) und Response-Modell (Indikator-Werte mit Timestamp)

## 4. Router / Endpunkte

- [ ] 4.1 `app/routers/time_series.py` implementieren: `GET /api/time-series` mit Validierung der Intervall-Werte
- [ ] 4.2 `app/routers/quote.py` implementieren: `GET /api/quote` mit Fehlerbehandlung für unbekannte Symbole
- [ ] 4.3 `app/routers/indicators.py` implementieren: `GET /api/indicators/{indicator}` mit Validierung der unterstützten Indikatoren (sma, ema, rsi) und Standard-Zeitperioden

## 5. App-Einstiegspunkt

- [ ] 5.1 `app/main.py` implementieren: FastAPI-App erstellen, alle Router registrieren, Lifespan für httpx-Client
- [ ] 5.2 Manuell testen: Uvicorn starten, Endpunkte mit Swagger UI (`/docs`) prüfen
