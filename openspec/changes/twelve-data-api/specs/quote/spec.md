## ADDED Requirements

### Requirement: Abruf des aktuellen Kurses
Das System SHALL einen GET-Endpunkt `/api/quote` bereitstellen, der den aktuellen Kurs und Marktdaten für ein angegebenes Symbol von Twelve Data abruft.

#### Scenario: Erfolgreicher Quote-Abruf
- **WHEN** ein Request an `GET /api/quote?symbol=AAPL` gesendet wird
- **THEN** gibt das System eine JSON-Response mit Status 200 zurück, die den aktuellen Kurs (open, high, low, close, volume), den Namen, die Börse und den Timestamp enthält

#### Scenario: Unbekanntes Symbol
- **WHEN** ein Request an `GET /api/quote?symbol=XXXINVALID` gesendet wird
- **THEN** gibt das System Status 404 mit einer Fehlermeldung zurück, die angibt, dass das Symbol nicht gefunden wurde

### Requirement: Validierung der Quote-Parameter
Das System SHALL den `symbol`-Parameter als Pflichtfeld validieren.

#### Scenario: Fehlendes Symbol
- **WHEN** ein Request an `GET /api/quote` ohne `symbol`-Parameter gesendet wird
- **THEN** gibt das System Status 422 mit einer Fehlermeldung zurück
