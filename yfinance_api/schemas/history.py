from pydantic import BaseModel


class OHLCVDataPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class HistoryResponse(BaseModel):
    symbol: str
    data: list[OHLCVDataPoint]
