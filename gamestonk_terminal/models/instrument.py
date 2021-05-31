# IMPORTATION STANDARD
from datetime import datetime

# IMPORTATION THIRDPARTY
import pandas as pd


class Instrument:
    def __init__(
        self,
        context: str = "stock",
        ticker: str = "GME",
        data: pd.DataFrame = None,
        interval: str = "1440min",
        prepost: bool = True,
        start: datetime = None,
        source: str = None,
    ) -> None:
        self.context = context
        self.ticker = ticker
        self.data = data
        self.interval = interval
        self.prepost = prepost
        self.start = start
        self.source = source
