from fastapi import APIRouter

from yfinance_api.schemas.info import TickerInfoResponse
from yfinance_api.services.yfinance_service import YFinanceService

router = APIRouter()
service = YFinanceService()


@router.get("/info/{symbol}", response_model=TickerInfoResponse)
def get_info(symbol: str) -> TickerInfoResponse:
    return service.get_info(symbol)
