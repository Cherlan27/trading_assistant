from pydantic import BaseModel


class QuoteResponse(BaseModel):
    symbol: str
    price: float | None = None
    currency: str | None = None
    exchange: str | None = None
    market_state: str | None = None
    previous_close: float | None = None
    open: float | None = None
    day_high: float | None = None
    day_low: float | None = None
    volume: int | None = None
    market_cap: int | None = None
