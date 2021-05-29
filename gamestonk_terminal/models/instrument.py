# IMPORTATION STANDARD
from datetime import datetime

# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL


class Instrument:
    def __init__(
        self,
        type:str="stock", # could be forex, crypto, etf
        ticker:str="GME",
        data:pd.DataFrame=None,
        interval:int="1440min",
        prepost:bool=True,
        start:datetime=None, # Default to 1 year ago or so
        source:str=None, # Source of data, default to Yahoo finance
    ) -> None:
        self.type = type
        self.ticker = ticker
        self.data = data
        self.interval = interval
        self.prepost = prepost
        self.start = start
        self.source = source