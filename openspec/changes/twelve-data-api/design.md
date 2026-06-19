## Context

Das Projekt hat noch keine Codebasis. Wir bauen eine FastAPI-Anwendung von Grund auf, die als Proxy/Wrapper für die Twelve Data REST API dient. Nutzer senden Anfragen mit einem Ticker-Symbol und erhalten strukturierte Marktdaten zurück.

Twelve Data bietet eine REST API mit JSON-Responses unter `https://api.twelvedata.com`. Authentifizierung erfolgt über einen API-Key als Query-Parameter (`apikey=...`). Der kostenlose Plan erlaubt 8 Requests/Minute und 800/Tag.

## Goals / Non-Goals

**Goals:**
- Saubere FastAPI-Projektstruktur mit klarer Trennung (Router, Services, Schemas)
- Typisierte Request/Response-Modelle mit Pydantic
- Zentraler HTTP-Client für Twelve Data mit Fehlerbehandlung
- API-Key sicher über Umgebungsvariablen verwalten
- Endpunkte für Time Series, Quote und technische Indikatoren

**Non-Goals:**
- Caching oder Datenbank-Persistierung (kommt später)
- Rate-Limiting auf unserer Seite
- Authentifizierung/Autorisierung für unsere API
- WebSocket-Streaming oder Echtzeit-Daten
- Frontend oder UI

## Decisions

### Projektstruktur: Modularer Aufbau mit `app/`-Package

```
app/
├── __init__.py
├── main.py              # FastAPI-App, Router-Registrierung
├── config.py            # Settings via pydantic-settings
├── routers/
│   ├── __init__.py
│   ├── time_series.py
│   ├── quote.py
│   └── indicators.py
├── schemas/
│   ├── __init__.py
│   ├── time_series.py
│   ├── quote.py
│   └── indicators.py
└── services/
    ├── __init__.py
    └── twelve_data.py   # HTTP-Client für Twelve Data
```

**Rationale:** Flache, aber getrennte Struktur. Router definieren Endpunkte, Schemas die Datenmodelle, Services die externe Kommunikation. Für ein Projekt dieser Größe ist ein einziger Service-Layer ausreichend.

### HTTP-Client: `httpx.AsyncClient`

**Rationale:** httpx ist der de-facto Standard für async HTTP in Python. Es unterstützt connection pooling, timeouts und passt natürlich zu FastAPI's async-Architektur. Alternative `aiohttp` bietet ähnliche Features, hat aber eine weniger ergonomische API.

### Konfiguration: `pydantic-settings` mit `.env`-Datei

**Rationale:** Pydantic-Settings lädt automatisch aus Umgebungsvariablen und `.env`-Dateien, bietet Typ-Validierung und ist bereits Teil des FastAPI-Ökosystems.

### Dependency Management: `pyproject.toml` mit poetry

**Rationale:** Das Dependendy Management soll mit Poetry erfolgen.

## Risks / Trade-offs

- **Twelve Data Rate Limits** → Kostenloser Plan hat 8 req/min. Bei vielen Anfragen werden 429-Fehler auftreten. Mitigation: Klare Fehlermeldungen an den Nutzer, Rate-Limiting kann in einem späteren Change hinzugefügt werden.
- **API-Key Exposure** → Key darf nicht in den Code oder Git gelangen. Mitigation: `.env`-Datei in `.gitignore`, Laden über Umgebungsvariablen.
- **Twelve Data API-Änderungen** → Externe API kann sich ändern. Mitigation: Zentraler Client als einzige Integrationsstelle, Pydantic-Schemas validieren Responses.
