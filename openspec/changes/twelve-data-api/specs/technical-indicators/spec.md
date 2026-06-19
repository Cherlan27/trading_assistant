## ADDED Requirements

### Requirement: Abruf technischer Indikatoren
Das System SHALL einen GET-Endpunkt `/api/indicators/{indicator}` bereitstellen, der technische Indikatoren (SMA, EMA, RSI) für ein angegebenes Symbol von Twelve Data abruft.

#### Scenario: Erfolgreicher SMA-Abruf
- **WHEN** ein Request an `GET /api/indicators/sma?symbol=AAPL&interval=1day&time_period=20` gesendet wird
- **THEN** gibt das System eine JSON-Response mit Status 200 zurück, die eine Liste von SMA-Werten mit Timestamp enthält

#### Scenario: Erfolgreicher RSI-Abruf
- **WHEN** ein Request an `GET /api/indicators/rsi?symbol=AAPL&interval=1day&time_period=14` gesendet wird
- **THEN** gibt das System eine JSON-Response mit Status 200 zurück, die eine Liste von RSI-Werten mit Timestamp enthält

#### Scenario: Nicht unterstützter Indikator
- **WHEN** ein Request an `GET /api/indicators/xyz?symbol=AAPL` gesendet wird
- **THEN** gibt das System Status 422 mit einer Fehlermeldung zurück, die die unterstützten Indikatoren auflistet (sma, ema, rsi)

### Requirement: Validierung der Indikator-Parameter
Das System SHALL die Eingabeparameter für Indikatoren validieren.

#### Scenario: Fehlendes Symbol
- **WHEN** ein Request an `GET /api/indicators/sma` ohne `symbol`-Parameter gesendet wird
- **THEN** gibt das System Status 422 mit einer Fehlermeldung zurück

#### Scenario: Standard-Zeitperiode
- **WHEN** ein Request an `GET /api/indicators/sma?symbol=AAPL&interval=1day` ohne `time_period` gesendet wird
- **THEN** verwendet das System einen Standard-Wert für `time_period` (20 für SMA/EMA, 14 für RSI)
