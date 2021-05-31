import pandas as pd
import pandas_ta as ta


def ema(data: pd.DataFrame, length: int = 20, offset: int = 0) -> pd.DataFrame:
    """Exponential Moving average

    The Exponential Moving Average is a staple of technical analysis and is used in countless
    technical indicators. In a Simple Moving Average, each value in the time period carries
    equal weight, and values outside of the time period are not included in the average.
    However, the Exponential Moving Average is a cumulative calculation, including all data.
    Past values have a diminishing contribution to the average, while more recent values have a
    greater contribution. This method allows the moving average to be more responsive to changes
    in the data.

    Parameters
    ----------
    data : DataFrame
        Dataframe where to apply EMA
    length : int
        Window size to use
    offset : int
        Vertical offset to use on data

    Returns
    -------
    pd.DataFrame
        Dataframe with data with EMA applied
    """
    return ta.ema(data, length=length, offset=offset).dropna()
