# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL
from gamestonk_terminal.models.instrument import Instrument
from gamestonk_terminal import config_terminal as cfg
from gamestonk_terminal.models.technical_analysis import (
    overlap,
    momentum,
    trend,
    volatility,
    volume,
    finbrain,
    tradingview,
)


class TechnicalAnalysis:
    def __init__(self, instrument: Instrument):
        self.instrument = instrument

    def ema(self, length: int, offset: int) -> pd.DataFrame:
        return overlap.ema(
            close=self.instrument.data["close"],
            length=length,
            offset=offset,
        )

    def sma(self, length: int, offset: int) -> pd.DataFrame:
        return overlap.sma(
            close=self.instrument.data["close"],
            length=length,
            offset=offset,
        )

    def vwap(self, offset: int) -> pd.DataFrame:
        return overlap.vwap(
            high=self.instrument.data["high"],
            low=self.instrument.data["low"],
            close=self.instrument.data["close"],
            volume=self.instrument.data["volume"],
            offset=offset,
        )

    def cci(self, length: int, scalar: int, offset: int) -> pd.DataFrame:
        return momentum.cci(
            high=self.instrument.data["high"],
            low=self.instrument.data["low"],
            close=self.instrument.data["close"],
            length=length,
            scalar=scalar,
            offset=offset,
        )

    def macd(self, fast: int, slow: int, signal: int, offset: int) -> pd.DataFrame:
        return momentum.macd(
            close=self.instrument.data["close"],
            fast=fast,
            slow=slow,
            signal=signal,
            offset=offset,
        )

    def rsi(self, length: int, scalar: int, drift: int, offset: int) -> pd.DataFrame:
        return momentum.rsi(
            close=self.instrument.data["close"],
            length=length,
            scalar=scalar,
            drift=drift,
            offset=offset,
        )

    def stoch(
        self, fastkperiod: int, slowdperiod: int, slowkperiod: int, offset: int
    ) -> pd.DataFrame:
        return momentum.stoch(
            high=self.instrument.data["high"],
            low=self.instrument.data["low"],
            close=self.instrument.data["close"],
            fastkperiod=fastkperiod,
            slowdperiod=slowdperiod,
            slowkperiod=slowkperiod,
            offset=offset,
        )

    def adx(self, length: int, scalar: int, drift: int, offset: int) -> pd.DataFrame:
        return trend.adx(
            high=self.instrument.data["high"],
            low=self.instrument.data["low"],
            close=self.instrument.data["close"],
            length=length,
            scalar=scalar,
            drift=drift,
            offset=offset,
        )

    def aroon(self, length: int, scalar: int, offset: int) -> pd.DataFrame:
        return trend.aroon(
            high=self.instrument.data["high"],
            low=self.instrument.data["low"],
            length=length,
            scalar=scalar,
            offset=offset,
        )

    def bbands(self, length: int, std: int, mamode: str, offset: int) -> pd.DataFrame:
        return volatility.bbands(
            close=self.instrument.data["close"],
            length=length,
            std=std,
            mamode=mamode,
            offset=offset,
        )

    def ad(self, offset: int, use_open: bool) -> pd.DataFrame:
        if use_open:
            return volume.ad_open(
                high=self.instrument.data["high"],
                low=self.instrument.data["low"],
                close=self.instrument.data["close"],
                volume=self.instrument.data["volume"],
                offset=offset,
                open_=self.instrument.data["open"],
            )

        return volume.ad(
            high=self.instrument.data["high"],
            low=self.instrument.data["low"],
            close=self.instrument.data["close"],
            volume=self.instrument.data["volume"],
            offset=offset,
        )

    def obv(self, offset: int) -> pd.DataFrame:
        return volume.obv(
            close=self.instrument.data["close"],
            volume=self.instrument.data["volume"],
            offset=offset,
        )

    def finbrain_technical_report(self) -> str:
        return finbrain.technical_report(
            ticker=self.instrument.ticker,
        )

    def tradingview_recommendation(
        self, screener: str, exchange: str, interval: str
    ) -> str:
        return tradingview.recommendation(
            API_KEY_ALPHAVANTAGE=cfg.API_KEY_ALPHAVANTAGE,
            ticker=self.instrument.ticker,
            screener=screener,
            exchange=exchange,
            interval=interval,
        )
