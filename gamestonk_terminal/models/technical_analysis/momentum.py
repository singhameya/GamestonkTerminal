import pandas as pd
import pandas_ta as ta


def cci(
    high: pd.DataFrame,
    low: pd.DataFrame,
    close: pd.DataFrame,
    length: int,
    scalar: int,
    offset: int,
) -> pd.DataFrame:
    return ta.cci(
        high=high,
        low=low,
        close=close,
        length=length,
        scalar=scalar,
        offset=offset,
    ).dropna()


def macd(
    close: pd.DataFrame,
    fast: int,
    slow: int,
    signal: int,
    offset: int,
) -> pd.DataFrame:
    return ta.macd(
        close=close,
        fast=fast,
        slow=slow,
        signal=signal,
        offset=offset,
    ).dropna()


def rsi(
    close: pd.DataFrame,
    length: int,
    scalar: int,
    drift: int,
    offset: int,
) -> pd.DataFrame:
    return ta.rsi(
        close=close,
        length=length,
        scalar=scalar,
        drift=drift,
        offset=offset,
    ).dropna()


def stoch(
    high: pd.DataFrame,
    low: pd.DataFrame,
    close: pd.DataFrame,
    fastkperiod: int,
    slowdperiod: int,
    slowkperiod: int,
    offset: int,
) -> pd.DataFrame:
    return ta.stoch(
        high=high,
        low=low,
        close=close,
        k=fastkperiod,
        d=slowdperiod,
        smooth_k=slowkperiod,
        offset=offset,
    ).dropna()
