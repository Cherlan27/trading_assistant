from typing import Literal

from fastapi import APIRouter, Query

from yfinance_api.schemas.history import HistoryResponse
from yfinance_api.services.yfinance_service import YFinanceService

router = APIRouter()
service = YFinanceService()

Period = Literal["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
Interval = Literal["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]


@router.get("/history/{symbol}", response_model=HistoryResponse)
def get_history(
    symbol: str,
    period: Period = Query(default="1mo"),
    interval: Interval = Query(default="1d"),
) -> HistoryResponse:
    return service.get_history(symbol, period=period, interval=interval)
