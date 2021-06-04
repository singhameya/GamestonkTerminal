import pandas as pd
import requests


def pattern_recognition(
    API_FINNHUB_KEY: str, ticker: str, resolution: str
) -> pd.DataFrame:
    """Get pattern recognition data

    Parameters
    ----------
    ticker : str
        Ticker to get pattern recognition data
    resolution : str
        Resolution of data to get pattern recognition from

    Returns
    -------
    pd.DataFrame
        Get datapoints corresponding to pattern signal data
    """
    response = requests.get(
        f"https://finnhub.io/api/v1/scan/pattern?symbol={ticker}&resolution={resolution}&token={API_FINNHUB_KEY}"
    )
    if response.status_code == 200:
        d_data = response.json()
        if "points" in d_data:
            return pd.DataFrame(d_data["points"]).T

    return pd.DataFrame()
