# IMPORTATION STANDARD
from datetime import datetime

# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL
from gamestonk_terminal.models.instrument import Instrument
import gamestonk_terminal.models.technical_analysis as ta
from gamestonk_terminal import config_terminal as cfg


class GamestonkTerminal:
    def __init__(
        self,
        context: str = "stock",  # could be forex, crypto, etf
        ticker: str = "GME",
        data: pd.DataFrame = pd.DataFrame(),
        interval: str = "1440min",
        prepost: bool = True,
        start: datetime = None,  # Default to 1 year ago or so
        source: str = None,  # Source of data, default to Yahoo finance
    ):
        self.cfg = cfg
        # The load could be done here. Everything would be provided except the data!
        self.instrument = Instrument(
            context, ticker, data, interval, prepost, start, source
        )
        if interval == "1440min":
            self.instrument.data.rename(
                columns={
                    "1. open": "open",
                    "2. high": "high",
                    "3. low": "low",
                    "5. adjusted close": "close",
                    "6. volume": "volume",
                },
                inplace=True,
            )
        else:
            self.instrument.data.rename(
                columns={
                    "1. open": "open",
                    "2. high": "high",
                    "3. low": "low",
                    "4. close": "close",
                    "6. volume": "volume",
                },
                inplace=True,
            )
        self.ta = ta.TechnicalAnalysis(instrument=self.instrument)
