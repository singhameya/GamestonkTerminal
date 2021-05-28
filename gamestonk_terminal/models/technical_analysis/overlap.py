# IMPORTATION THIRDPARTY
import matplotlib.pyplot as plt
import pandas_ta as ta

from pandas.plotting import register_matplotlib_converters

# IMPORTATION INTERNAL
from gamestonk_terminal.helper_funcs import (
    plot_autoscale,
)
from gamestonk_terminal.config_plot import PLOT_DPI

register_matplotlib_converters()

def ema(s_ticker, s_interval, df_stock, n_length, n_offset):
    # Daily
    if s_interval == "1440min":
        df_ta = ta.ema(
            df_stock["5. adjusted close"],
            length=n_length,
            offset=n_offset,
        ).dropna()

    # Intraday
    else:
        df_ta = ta.ema(
            df_stock["4. close"],
            length=n_length,
            offset=n_offset,
        ).dropna()

    _, _ = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    plt.title(f"{n_length} EMA on {s_ticker}")
    if s_interval == "1440min":
        plt.plot(
            df_stock["5. adjusted close"].index,
            df_stock["5. adjusted close"].values,
            "k",
            lw=3,
        )
        plt.xlim(
            df_stock["5. adjusted close"].index[0],
            df_stock["5. adjusted close"].index[-1],
        )
    else:
        plt.plot(df_stock["4. close"].index, df_stock["4. close"].values, "k", lw=3)
        plt.xlim(df_stock["4. close"].index[0], df_stock["4. close"].index[-1])
    plt.xlabel("Time")
    plt.ylabel(f"Share Price of {s_ticker} ($)")
    plt.plot(df_ta.index, df_ta.values, c="tab:blue")
    l_legend = list()
    l_legend.append(s_ticker)
    # Pandas series
    if len(df_ta.shape) == 1:
        l_legend.append(f"{n_length} EMA")
    # Pandas dataframe
    else:
        l_legend.append(df_ta.columns.tolist())
    plt.legend(l_legend)
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)

    return plt