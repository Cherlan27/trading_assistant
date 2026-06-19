## ADDED Requirements

### Requirement: HTTP-Client für Twelve Data API
Das System SHALL einen zentralen async HTTP-Client bereitstellen, der alle Anfragen an die Twelve Data API (`https://api.twelvedata.com`) bündelt und den API-Key automatisch anhängt.

#### Scenario: Erfolgreicher API-Aufruf
- **WHEN** der Client eine Anfrage an einen Twelve Data Endpunkt sendet
- **THEN** wird der API-Key als Query-Parameter `apikey` angefügt und die JSON-Response zurückgegeben

#### Scenario: API-Key nicht konfiguriert
- **WHEN** die Anwendung ohne gesetzten `TWELVE_DATA_API_KEY` gestartet wird
- **THEN** schlägt der Start mit einer Fehlermeldung fehl, die auf die fehlende Konfiguration hinweist

### Requirement: Fehlerbehandlung für Twelve Data Responses
Das System SHALL Fehlerfälle der Twelve Data API erkennen und als HTTP-Fehler an den Aufrufer weitergeben.

#### Scenario: Twelve Data gibt einen Fehler zurück
- **WHEN** Twelve Data eine Response mit `status: "error"` zurückgibt
- **THEN** gibt der Client einen entsprechenden HTTP-Fehler mit der Fehlermeldung von Twelve Data weiter

#### Scenario: Netzwerk-Timeout
- **WHEN** die Anfrage an Twelve Data nach 10 Sekunden keine Antwort erhält
- **THEN** gibt der Client einen HTTP 504 Gateway Timeout zurück

#### Scenario: Twelve Data Rate Limit erreicht
- **WHEN** Twelve Data mit HTTP 429 antwortet
- **THEN** gibt der Client HTTP 429 mit einer Fehlermeldung an den Aufrufer weiter, die auf das Rate Limit hinweist
