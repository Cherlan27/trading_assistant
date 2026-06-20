import pandas as pd

from yfinance_api.schemas.indicators import (
    BollingerDataPoint,
    IndicatorDataPoint,
    MACDDataPoint,
)


class IndicatorService:
    def compute_sma(self, df: pd.DataFrame, window: int) -> list[IndicatorDataPoint]:
        sma = df["Close"].rolling(window=window).mean()
        return self._to_data_points(df, sma)

    def compute_ema(self, df: pd.DataFrame, window: int) -> list[IndicatorDataPoint]:
        ema = df["Close"].ewm(span=window, adjust=False).mean()
        return self._to_data_points(df, ema)

    def compute_rsi(self, df: pd.DataFrame, period: int) -> list[IndicatorDataPoint]:
        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = (-delta).where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return self._to_data_points(df, rsi)

    def compute_macd(self, df: pd.DataFrame) -> list[MACDDataPoint]:
        ema12 = df["Close"].ewm(span=12, adjust=False).mean()
        ema26 = df["Close"].ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line

        results = []
        for i in range(len(df)):
            if pd.isna(macd_line.iloc[i]) or pd.isna(signal_line.iloc[i]):
                continue
            results.append(
                MACDDataPoint(
                    date=str(df.index[i].date()),
                    macd=round(macd_line.iloc[i], 6),
                    signal=round(signal_line.iloc[i], 6),
                    histogram=round(histogram.iloc[i], 6),
                )
            )
        return results

    def compute_bbands(self, df: pd.DataFrame, window: int) -> list[BollingerDataPoint]:
        sma = df["Close"].rolling(window=window).mean()
        std = df["Close"].rolling(window=window).std()
        upper = sma + 2 * std
        lower = sma - 2 * std

        results = []
        for i in range(len(df)):
            if pd.isna(sma.iloc[i]):
                continue
            results.append(
                BollingerDataPoint(
                    date=str(df.index[i].date()),
                    upper=round(upper.iloc[i], 6),
                    middle=round(sma.iloc[i], 6),
                    lower=round(lower.iloc[i], 6),
                )
            )
        return results

    def _to_data_points(self, df: pd.DataFrame, series: pd.Series) -> list[IndicatorDataPoint]:
        results = []
        for i in range(len(df)):
            if pd.isna(series.iloc[i]):
                continue
            results.append(
                IndicatorDataPoint(
                    date=str(df.index[i].date()),
                    value=round(series.iloc[i], 6),
                )
            )
        return results
