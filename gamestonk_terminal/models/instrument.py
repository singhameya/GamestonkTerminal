# IMPORTATION STANDARD
from datetime import datetime

# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL


class Instrument:
    def __init__(
        self,
        ticker:str=None,
        interval:int=None,
        prepost:bool=None,
        start:datetime=None,
        source:str=None,
    ) -> None:

        pass