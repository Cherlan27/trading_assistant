import yfinance as yf
from fastapi import HTTPException
from requests.exceptions import ConnectionError, Timeout

from yfinance_api.schemas.history import HistoryResponse, OHLCVDataPoint
from yfinance_api.schemas.info import TickerInfoResponse
from yfinance_api.schemas.quote import QuoteResponse


class YFinanceService:
    def get_quote(self, symbol: str) -> QuoteResponse:
        ticker = self._get_ticker(symbol)
        try:
            info = ticker.info
        except (ConnectionError, Timeout, OSError) as e:
            raise HTTPException(status_code=502, detail=f"Upstream service unavailable: {e}")

        if not info or info.get("regularMarketPrice") is None:
            raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")

        return QuoteResponse(
            symbol=symbol.upper(),
            price=info.get("regularMarketPrice") or info.get("currentPrice"),
            currency=info.get("currency"),
            exchange=info.get("exchange"),
            market_state=info.get("marketState"),
            previous_close=info.get("regularMarketPreviousClose") or info.get("previousClose"),
            open=info.get("regularMarketOpen") or info.get("open"),
            day_high=info.get("regularMarketDayHigh") or info.get("dayHigh"),
            day_low=info.get("regularMarketDayLow") or info.get("dayLow"),
            volume=info.get("regularMarketVolume") or info.get("volume"),
            market_cap=info.get("marketCap"),
        )

    def get_history(self, symbol: str, period: str = "1mo", interval: str = "1d") -> HistoryResponse:
        ticker = self._get_ticker(symbol)
        try:
            df = ticker.history(period=period, interval=interval)
        except (ConnectionError, Timeout, OSError) as e:
            raise HTTPException(status_code=502, detail=f"Upstream service unavailable: {e}")

        if df.empty:
            raise HTTPException(status_code=404, detail=f"No historical data found for symbol '{symbol}'")

        data_points = [
            OHLCVDataPoint(
                date=index.isoformat(),
                open=row["Open"],
                high=row["High"],
                low=row["Low"],
                close=row["Close"],
                volume=int(row["Volume"]),
            )
            for index, row in df.iterrows()
        ]

        return HistoryResponse(symbol=symbol.upper(), data=data_points)

    def get_info(self, symbol: str) -> TickerInfoResponse:
        ticker = self._get_ticker(symbol)
        try:
            info = ticker.info
        except (ConnectionError, Timeout, OSError) as e:
            raise HTTPException(status_code=502, detail=f"Upstream service unavailable: {e}")

        if not info or not info.get("shortName"):
            raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")

        return TickerInfoResponse(
            symbol=symbol.upper(),
            name=info.get("shortName") or info.get("longName"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            market_cap=info.get("marketCap"),
            currency=info.get("currency"),
            exchange=info.get("exchange"),
            description=info.get("longBusinessSummary"),
            dividend_rate=info.get("dividendRate"),
            dividend_yield=info.get("dividendYield"),
        )

    def _get_ticker(self, symbol: str) -> yf.Ticker:
        return yf.Ticker(symbol)
