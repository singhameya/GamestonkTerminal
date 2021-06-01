import pandas as pd
import pandas_ta as ta


def bbands(
    close: pd.DataFrame,
    length: int,
    std: int,
    mamode: str,
    offset: int,
) -> pd.DataFrame:
    return ta.bbands(
        close=close,
        length=length,
        std=std,
        mamode=mamode,
        offset=offset,
    ).dropna()
