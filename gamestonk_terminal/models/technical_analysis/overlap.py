import pandas as pd
import pandas_ta as ta


def ema(close: pd.DataFrame, length: int = 20, offset: int = 0) -> pd.DataFrame:
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
    return ta.ema(close, length=length, offset=offset).dropna()


def sma(close: pd.DataFrame, length: int = 20, offset: int = 0) -> pd.DataFrame:
    """Simple Moving average

    Moving Averages are used to smooth the data in an array to help eliminate noise
    and identify trends. The Simple Moving Average is literally the simplest form of
    a moving average. Each output value is the average of the previous n values.
    In a Simple Moving Average, each value in the time period carries equal weight,
    and values outside of the time period are not included in the average. This makes
    it less responsive to recent changes in the data, which can be useful for filtering
    out those changes.

    Parameters
    ----------
    data : DataFrame
        Dataframe where to apply SMA
    length : int
        Window size to use
    offset : int
        Vertical offset to use on data

    Returns
    -------
    pd.DataFrame
        Dataframe with data with EMA applied
    """
    return ta.sma(close, length=length, offset=offset).dropna()


def vwap(
    high: pd.DataFrame,
    low: pd.DataFrame,
    close: pd.DataFrame,
    volume: pd.DataFrame,
    offset: int = 0,
) -> pd.DataFrame:
    """Volume Weighted Average Price

    The VWAP that measures the average typical price by volume.
    It is typically used with intraday charts to identify general direction.

    Parameters
    ----------
    high : DataFrame
        High price
    low : DataFrame
        Low price
    close : DataFrame
        Closing price
    volume : DataFrame
        Volume
    offset : int
        Vertical offset to use on data

    Returns
    -------
    pd.DataFrame
        Dataframe with data with EMA applied
    """
    return ta.vwap(
        high=high,
        low=low,
        close=close,
        volume=volume,
        offset=offset,
    )
