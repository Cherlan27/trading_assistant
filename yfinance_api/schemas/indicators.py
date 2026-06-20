from pydantic import BaseModel


class IndicatorDataPoint(BaseModel):
    date: str
    value: float


class MACDDataPoint(BaseModel):
    date: str
    macd: float
    signal: float
    histogram: float


class BollingerDataPoint(BaseModel):
    date: str
    upper: float
    middle: float
    lower: float


class IndicatorsResponse(BaseModel):
    symbol: str
    indicators: dict[str, list[IndicatorDataPoint | MACDDataPoint | BollingerDataPoint]]
