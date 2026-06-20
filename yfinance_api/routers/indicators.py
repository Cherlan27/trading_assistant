import re
from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from yfinance_api.schemas.indicators import IndicatorsResponse
from yfinance_api.services.indicator_service import IndicatorService
from yfinance_api.services.yfinance_service import YFinanceService

router = APIRouter()
yf_service = YFinanceService()
indicator_service = IndicatorService()

VALID_INDICATOR_PATTERN = re.compile(r"^(sma|ema|rsi|bbands)_\d+$")
VALID_INDICATORS = {"macd"}

Period = Literal["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
Interval = Literal["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]


def _parse_indicator(name: str) -> tuple[str, int | None]:
    if name == "macd":
        return ("macd", None)
    match = VALID_INDICATOR_PATTERN.match(name)
    if not match:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid indicator: '{name}'. Expected format: sma_20, ema_50, rsi_14, bbands_20, or macd",
        )
    indicator_type, param = name.rsplit("_", 1)
    return (indicator_type, int(param))


@router.get("/indicators/{symbol}", response_model=IndicatorsResponse)
def get_indicators(
    symbol: str,
    period: Period = Query(default="1y"),
    interval: Interval = Query(default="1d"),
    indicators: str = Query(default=""),
) -> IndicatorsResponse:
    if not indicators.strip():
        return IndicatorsResponse(symbol=symbol.upper(), indicators={})

    indicator_list = [s.strip() for s in indicators.split(",") if s.strip()]

    parsed = []
    for name in indicator_list:
        parsed.append((name, *_parse_indicator(name)))

    history = yf_service.get_history(symbol, period=period, interval=interval)
    import pandas as pd

    df = pd.DataFrame(
        [{"Open": d.open, "High": d.high, "Low": d.low, "Close": d.close, "Volume": d.volume} for d in history.data],
        index=pd.to_datetime([d.date for d in history.data], utc=True),
    )

    results: dict = {}
    for name, indicator_type, param in parsed:
        if indicator_type == "sma":
            results[name] = indicator_service.compute_sma(df, param)
        elif indicator_type == "ema":
            results[name] = indicator_service.compute_ema(df, param)
        elif indicator_type == "rsi":
            results[name] = indicator_service.compute_rsi(df, param)
        elif indicator_type == "macd":
            results[name] = indicator_service.compute_macd(df)
        elif indicator_type == "bbands":
            results[name] = indicator_service.compute_bbands(df, param)

    return IndicatorsResponse(symbol=symbol.upper(), indicators=results)
