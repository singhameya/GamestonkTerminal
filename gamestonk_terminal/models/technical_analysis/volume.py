import pandas as pd
import pandas_ta as ta


def ad(
    high: pd.DataFrame,
    low: pd.DataFrame,
    close: pd.DataFrame,
    volume: pd.DataFrame,
    offset: int,
) -> pd.DataFrame:
    return ta.ad(
        high=high,
        low=low,
        close=close,
        volume=volume,
        offset=offset,
    ).dropna()


def ad_open(
    high: pd.DataFrame,
    low: pd.DataFrame,
    close: pd.DataFrame,
    volume: pd.DataFrame,
    offset: int,
    open_: pd.DataFrame,
) -> pd.DataFrame:
    return ta.ad(
        high=high,
        low=low,
        close=close,
        volume=volume,
        offset=offset,
        open_=open_,
    ).dropna()


def obv(
    close: pd.DataFrame,
    volume: pd.DataFrame,
    offset: int,
) -> pd.DataFrame:
    return ta.obv(
        close=close,
        volume=volume,
        offset=offset,
    ).dropna()
