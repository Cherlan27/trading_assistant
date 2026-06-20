from pydantic import BaseModel


class TickerInfoResponse(BaseModel):
    symbol: str
    name: str | None = None
    sector: str | None = None
    industry: str | None = None
    market_cap: int | None = None
    currency: str | None = None
    exchange: str | None = None
    description: str | None = None
    dividend_rate: float | None = None
    dividend_yield: float | None = None
