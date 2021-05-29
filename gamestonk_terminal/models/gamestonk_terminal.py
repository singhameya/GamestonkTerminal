# IMPORTATION STANDARD
from datetime import datetime
from gamestonk_terminal.models.instrument import Instrument

# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL
import gamestonk_terminal.models.technical_analysis as ta
from gamestonk_terminal import config_terminal as cfg

gst = None

def getGST():
    global gst

    if gst is not None:
        return gst
    else:
        gst = GamestonkTerminal()
        return gst

class GamestonkTerminal:
    def __init__(self,
        type:str="stock", # could be forex, crypto, etf
        ticker:str="GME",
        data:pd.DataFrame=None,
        interval:int="1440min",
        prepost:bool=True,
        start:datetime=None, # Default to 1 year ago or so
        source:str=None, # Source of data, default to Yahoo finance
    ):
        self.cfg = cfg
        self.instrument = Instrument(type, ticker, data, interval, prepost, start, source)
        self.ta = ta.TechnicalAnalysis(instrument=self.instrument)

    def clear(
        self,
        ticker:str,
        start:datetime,
        interval:int,
    ):
        pass