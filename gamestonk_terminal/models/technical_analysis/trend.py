import pandas as pd
import pandas_ta as ta


def adx(
    high: pd.DataFrame,
    low: pd.DataFrame,
    close: pd.DataFrame,
    length: int,
    scalar: int,
    drift: int,
    offset: int,
) -> pd.DataFrame:
    return ta.adx(
        high=high,
        low=low,
        close=close,
        length=length,
        scalar=scalar,
        drift=drift,
        offset=offset,
    ).dropna()


def aroon(
    high: pd.DataFrame,
    low: pd.DataFrame,
    length: int,
    scalar: int,
    offset: int,
) -> pd.DataFrame:
    return ta.aroon(
        high=high,
        low=low,
        length=length,
        scalar=scalar,
        offset=offset,
    ).dropna()
