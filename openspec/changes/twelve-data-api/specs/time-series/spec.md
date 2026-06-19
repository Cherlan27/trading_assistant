## ADDED Requirements

### Requirement: Abruf historischer Zeitreihen-Daten
Das System SHALL einen GET-Endpunkt `/api/time-series` bereitstellen, der historische OHLCV-Kursdaten (Open, High, Low, Close, Volume) für ein angegebenes Symbol von Twelve Data abruft und als JSON zurückgibt.

#### Scenario: Erfolgreicher Abruf mit Standardparametern
- **WHEN** ein Request an `GET /api/time-series?symbol=AAPL` gesendet wird
- **THEN** gibt das System eine JSON-Response mit Status 200 zurück, die eine Liste von OHLCV-Datenpunkten mit Timestamp enthält, sortiert nach Datum absteigend

#### Scenario: Abruf mit benutzerdefiniertem Intervall
- **WHEN** ein Request an `GET /api/time-series?symbol=AAPL&interval=1h` gesendet wird
- **THEN** gibt das System OHLCV-Daten im 1-Stunden-Intervall zurück

#### Scenario: Abruf mit Zeitraum-Einschränkung
- **WHEN** ein Request an `GET /api/time-series?symbol=AAPL&start_date=2024-01-01&end_date=2024-06-01` gesendet wird
- **THEN** gibt das System nur Datenpunkte innerhalb des angegebenen Zeitraums zurück

### Requirement: Validierung der Time-Series-Parameter
Das System SHALL die Eingabeparameter validieren und bei ungültigen Werten einen Fehler zurückgeben.

#### Scenario: Fehlendes Symbol
- **WHEN** ein Request an `GET /api/time-series` ohne `symbol`-Parameter gesendet wird
- **THEN** gibt das System Status 422 mit einer Fehlermeldung zurück, die das fehlende Feld benennt

#### Scenario: Ungültiges Intervall
- **WHEN** ein Request an `GET /api/time-series?symbol=AAPL&interval=invalid` gesendet wird
- **THEN** gibt das System Status 422 mit einer Fehlermeldung zurück, die die gültigen Intervalle auflistet
