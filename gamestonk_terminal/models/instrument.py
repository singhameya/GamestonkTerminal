import pandas as pd


class Instrument:
    context = ""
    ticker = ""
    source = ""
    interval = 0
    repost = False
    start = None
    data = pd.DataFrame()
