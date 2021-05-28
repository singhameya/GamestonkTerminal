# IMPORTATION STANDARD
from datetime import datetime
import pandas_ta as ta

# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL
from gamestonk_terminal.models.instrument import Instrument


class TechnicalAnalysis:
    def __init__(self, instrument:Instrument):
        self.instrument = instrument

    def ema(self, length:int, offset:int)-> pd.DataFrame:
        df_ta = ta.ema(
            df_stock["5. adjusted close"],
            length=n_length,
            offset=n_offset,
        ).dropna()
