# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL
from gamestonk_terminal.models.instrument import Instrument
from gamestonk_terminal.models.technical_analysis import overlap


class TechnicalAnalysis:
    def __init__(self, instrument: Instrument):
        self.instrument = instrument

    def ema(self, length: int, offset: int) -> pd.DataFrame:
        if self.instrument.interval == "1440min":
            return overlap.ema(
                self.instrument.data["5. adjusted close"], length, offset
            )
        return overlap.ema(self.instrument.data["4. close"], length, offset)
