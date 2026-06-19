## Why

Das Projekt braucht eine API-Schicht, um Marktdaten von Twelve Data abzufragen. Nutzer sollen per HTTP-Endpunkt ein Ticker-Symbol angeben und strukturierte Kursdaten (Zeitreihen, Quotes, technische Indikatoren) zurückerhalten, ohne direkt mit der Twelve Data API interagieren zu müssen.

## What Changes

- Neue FastAPI-Anwendung mit Projektstruktur (App-Modul, Router, Config, Schemas)
- Endpunkte zum Abrufen von Zeitreihen-Daten (Time Series) nach Symbol und Intervall
- Endpunkt für aktuelle Quotes (Echtzeitkurs) nach Symbol
- Endpunkt für technische Indikatoren (z. B. SMA, EMA, RSI) nach Symbol
- Integration mit der Twelve Data REST API über einen HTTP-Client
- API-Key-Verwaltung über Umgebungsvariablen
- Pydantic-Schemas für Request-Validierung und Response-Modelle

## Capabilities

### New Capabilities
- `time-series`: Abruf historischer Kursdaten (OHLCV) für ein Symbol mit konfigurierbarem Intervall und Zeitraum
- `quote`: Abruf des aktuellen Kurses und Marktdaten für ein Symbol
- `technical-indicators`: Abruf technischer Indikatoren (SMA, EMA, RSI) für ein Symbol
- `twelve-data-client`: HTTP-Client-Wrapper für die Twelve Data API mit Fehlerbehandlung und API-Key-Management

### Modified Capabilities

## Impact

- Neue Python-Abhängigkeiten: FastAPI, Uvicorn, httpx, Pydantic
- Twelve Data API-Key wird als Umgebungsvariable (`TWELVE_DATA_API_KEY`) benötigt
- Neues App-Verzeichnis `app/` mit Modulstruktur (routers, schemas, services, config)
