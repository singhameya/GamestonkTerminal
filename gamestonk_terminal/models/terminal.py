# IMPORTATION STANDARD
from datetime import datetime

# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL
import gamestonk_terminal.models.technical_analysis as ta

tm = None

def getTerminal():
    global tm

    if tm is not None:
        return tm
    else:
        tm = Terminal()
        return tm

class Terminal:
    def __init__(self):
        self.ta = ta
        self.__df_stock = pd.DataFrame()

    def load(
        self,
        ticker:str,
        start:datetime,
        interval:int,
        source:str,
        prepost:bool,
    ):
        pass

    def clear(
        self,
        ticker:str,
        start:datetime,
        interval:int,
    ):
        pass