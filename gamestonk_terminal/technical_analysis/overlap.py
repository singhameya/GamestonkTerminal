from typing import List
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from gamestonk_terminal.helper_funcs import (
    plot_autoscale,
)
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.models import gamestonk_terminal

register_matplotlib_converters()


def ema(gst: gamestonk_terminal.GamestonkTerminal, length: List[int], offset: int):
    fig, _ = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    if gst.instrument.interval == "1440min":
        plt.plot(
            gst.instrument.data.index,
            gst.instrument.data["5. adjusted close"].values,
            color="k",
        )
    else:
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["4. close"].values, color="k"
        )
    l_legend = list()
    l_legend.append(gst.instrument.ticker)

    for leng in length:
        df_ta = gst.ta.ema(length=leng, offset=offset)
        plt.plot(df_ta.index, df_ta.values)
        l_legend.append(f"{leng} EMA")

    plt.title(f"EMA on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.xlabel("Time")
    plt.ylabel("Share Price ($)")
    plt.legend(l_legend)
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)

    return fig


def sma(gst: gamestonk_terminal.GamestonkTerminal, length: List[int], offset: int):
    fig, _ = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    if gst.instrument.interval == "1440min":
        plt.plot(
            gst.instrument.data.index,
            gst.instrument.data["5. adjusted close"].values,
            color="k",
        )
    else:
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["4. close"].values, color="k"
        )
    l_legend = list()
    l_legend.append(gst.instrument.ticker)

    for leng in length:
        df_ta = gst.ta.sma(length=leng, offset=offset)
        plt.plot(df_ta.index, df_ta.values)
        l_legend.append(f"{leng} SMA")

    plt.title(f"SMA on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.xlabel("Time")
    plt.ylabel("Share Price ($)")
    plt.legend(l_legend)
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)

    return fig


def vwap(gst: gamestonk_terminal.GamestonkTerminal, offset: int):
    fig, _ = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.vwap(offset=offset)

    _, axPrice = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    if gst.instrument.interval == "1440min":
        plt.plot(
            gst.instrument.data.index,
            gst.instrument.data["5. adjusted close"].values,
            color="k",
        )
    else:
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["4. close"].values, color="k"
        )
    plt.plot(df_ta.index, df_ta.values)
    plt.title(f"VWAP on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.xlabel("Time")
    plt.ylabel("Share Price ($)")
    plt.legend([gst.instrument.ticker, "VWAP"])
    _ = axPrice.twinx()
    if gst.instrument.interval == "1440min":
        plt.bar(
            gst.instrument.data.index,
            gst.instrument.data["6. volume"].values,
            color="k",
            alpha=0.8,
            width=0.3,
        )
    else:
        plt.bar(
            gst.instrument.data.index,
            gst.instrument.data["5. volume"].values,
            color="k",
            alpha=0.8,
            width=0.3,
        )
    plt.ylabel("Volume")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)

    return fig
