# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL
from gamestonk_terminal.models.instrument import Instrument
from gamestonk_terminal.models.technical_analysis import overlap, momentum


class TechnicalAnalysis:
    def __init__(self, instrument: Instrument):
        self.instrument = instrument

    def ema(self, length: int, offset: int) -> pd.DataFrame:
        if self.instrument.interval == "1440min":
            return overlap.ema(
                close=self.instrument.data["5. adjusted close"],
                length=length,
                offset=offset,
            )
        return overlap.ema(self.instrument.data["4. close"], length, offset)

    def sma(self, length: int, offset: int) -> pd.DataFrame:
        if self.instrument.interval == "1440min":
            return overlap.sma(
                close=self.instrument.data["5. adjusted close"],
                length=length,
                offset=offset,
            )
        return overlap.sma(self.instrument.data["4. close"], length, offset)

    def vwap(self, offset: int) -> pd.DataFrame:
        if self.instrument.interval == "1440min":
            return overlap.vwap(
                high=self.instrument.data["2. high"],
                low=self.instrument.data["3. low"],
                close=self.instrument.data["5. adjusted close"],
                volume=self.instrument.data["6. volume"],
                offset=offset,
            )
        return overlap.vwap(
            high=self.instrument.data["2. high"],
            low=self.instrument.data["3. low"],
            close=self.instrument.data["4. close"],
            volume=self.instrument.data["6. volume"],
            offset=offset,
        )

    def cci(self, length: int, scalar: int, offset: int) -> pd.DataFrame:
        if self.instrument.interval == "1440min":
            return momentum.cci(
                high=self.instrument.data["2. high"],
                low=self.instrument.data["3. low"],
                close=self.instrument.data["5. adjusted close"],
                length=length,
                scalar=scalar,
                offset=offset,
            )
        return momentum.cci(
            high=self.instrument.data["2. high"],
            low=self.instrument.data["3. low"],
            close=self.instrument.data["4. close"],
            length=length,
            scalar=scalar,
            offset=offset,
        )

    def macd(self, fast: int, slow: int, signal: int, offset: int) -> pd.DataFrame:
        if self.instrument.interval == "1440min":
            return momentum.macd(
                close=self.instrument.data["5. adjusted close"],
                fast=fast,
                slow=slow,
                signal=signal,
                offset=offset,
            )
        return momentum.macd(
            close=self.instrument.data["4. close"],
            fast=fast,
            slow=slow,
            signal=signal,
            offset=offset,
        )

    def rsi(self, length: int, scalar: int, drift: int, offset: int) -> pd.DataFrame:
        if self.instrument.interval == "1440min":
            return momentum.rsi(
                close=self.instrument.data["5. adjusted close"],
                length=length,
                scalar=scalar,
                drift=drift,
                offset=offset,
            )
        return momentum.rsi(
            close=self.instrument.data["4. close"],
            length=length,
            scalar=scalar,
            drift=drift,
            offset=offset,
        )

    def stoch(
        self, fastkperiod: int, slowdperiod: int, slowkperiod: int, offset: int
    ) -> pd.DataFrame:
        if self.instrument.interval == "1440min":
            return momentum.stoch(
                high=self.instrument.data["2. high"],
                low=self.instrument.data["3. low"],
                close=self.instrument.data["5. adjusted close"],
                fastkperiod=fastkperiod,
                slowdperiod=slowdperiod,
                slowkperiod=slowkperiod,
                offset=offset,
            )
        return momentum.stoch(
            high=self.instrument.data["2. high"],
            low=self.instrument.data["3. low"],
            close=self.instrument.data["4. close"],
            fastkperiod=fastkperiod,
            slowdperiod=slowdperiod,
            slowkperiod=slowkperiod,
            offset=offset,
        )
