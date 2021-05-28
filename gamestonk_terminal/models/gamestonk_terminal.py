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
    def __init__(self):
        self.cfg = cfg
        self.intrument = Instrument()
        self.ta = ta.TechnicalAnalysis(instrument=self.intrument)
        self.__df_stock = pd.DataFrame()

    def load(
        self,
        intrument:Instrument,
    ):
        self.intrument = intrument

    def clear(
        self,
        ticker:str,
        start:datetime,
        interval:int,
    ):
        pass