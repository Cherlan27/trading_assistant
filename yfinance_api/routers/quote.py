from fastapi import APIRouter

from yfinance_api.schemas.quote import QuoteResponse
from yfinance_api.services.yfinance_service import YFinanceService

router = APIRouter()
service = YFinanceService()


@router.get("/quote/{symbol}", response_model=QuoteResponse)
def get_quote(symbol: str) -> QuoteResponse:
    return service.get_quote(symbol)
