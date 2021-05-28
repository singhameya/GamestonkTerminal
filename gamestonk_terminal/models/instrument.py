# IMPORTATION STANDARD
from datetime import datetime

# IMPORTATION THIRDPARTY
import pandas as pd

# IMPORTATION INTERNAL


class Instrument:
    def __init__(
        self,
        ticker:str,
        interval:int,
        prepost:bool,
        start:datetime=None,
        source:str=None,
    ) -> None:

        pass