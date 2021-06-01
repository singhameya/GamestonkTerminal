import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from gamestonk_terminal.helper_funcs import (
    plot_autoscale,
)
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.models import gamestonk_terminal

register_matplotlib_converters()


def plot_ad(
    gst: gamestonk_terminal.GamestonkTerminal,
    offset: int,
    use_open: bool,
):
    fig = plt.figure(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.ad(offset, use_open)

    axPrice = plt.subplot(211)
    plt.plot(gst.instrument.data.index, gst.instrument.data["close"].values, "k", lw=2)
    plt.title(f"Accumulation/Distribution Line (AD) on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.ylabel("Share Price ($)")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    _ = axPrice.twinx()
    plt.bar(
        gst.instrument.data.index,
        gst.instrument.data["volume"].values,
        color="k",
        alpha=0.8,
        width=0.3,
    )
    plt.subplot(212)
    plt.plot(df_ta.index, df_ta.values, "b", lw=1)
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.axhline(0, linewidth=2, color="k", ls="--")
    plt.legend(["Chaikin Oscillator"])
    plt.xlabel("Time")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)

    return fig


def plot_obv(
    gst: gamestonk_terminal.GamestonkTerminal,
    offset: int,
):
    fig = plt.figure(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.obv(offset)

    axPrice = plt.subplot(211)
    plt.plot(
        gst.instrument.data.index, gst.instrument.data["4. close"].values, "k", lw=2
    )
    plt.title(f"On-Balance Volume (OBV) on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.ylabel("Share Price ($)")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    _ = axPrice.twinx()
    plt.bar(
        gst.instrument.data.index,
        gst.instrument.data["volume"].values,
        color="k",
        alpha=0.8,
        width=0.3,
    )
    plt.subplot(212)
    plt.plot(df_ta.index, df_ta.values, "b", lw=1)
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.legend(["OBV"])
    plt.xlabel("Time")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)

    return fig
