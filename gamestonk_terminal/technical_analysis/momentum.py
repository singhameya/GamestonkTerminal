import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from gamestonk_terminal.helper_funcs import (
    plot_autoscale,
)
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.models import gamestonk_terminal

register_matplotlib_converters()


def cci(
    gst: gamestonk_terminal.GamestonkTerminal, length: int, scalar: int, offset: int
):

    fig, _ = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.cci(length=length, scalar=scalar, offset=offset)

    plt.subplot(211)
    plt.title(f"Commodity Channel Index (CCI) on {gst.instrument.ticker}")
    if gst.instrument.interval == "1440min":
        plt.plot(
            gst.instrument.data.index,
            gst.instrument.data["5. adjusted close"].values,
            "k",
            lw=2,
        )
    else:
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["4. close"].values, "k", lw=2
        )

    plt.ylabel("Share Price ($)")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.subplot(212)
    plt.plot(df_ta.index, df_ta.values, "b", lw=2)
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.axhspan(100, plt.gca().get_ylim()[1], facecolor="r", alpha=0.2)
    plt.axhspan(plt.gca().get_ylim()[0], -100, facecolor="g", alpha=0.2)
    plt.axhline(100, linewidth=3, color="r", ls="--")
    plt.axhline(-100, linewidth=3, color="g", ls="--")
    plt.xlabel("Time")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.gca().twinx()
    plt.ylim(plt.gca().get_ylim())
    plt.yticks([0.2, 0.8], ("OVERSOLD", "OVERBOUGHT"))

    return fig


def macd(
    gst: gamestonk_terminal.GamestonkTerminal,
    fast: int,
    slow: int,
    signal: int,
    offset: int,
):
    fig, _ = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.macd(fast=fast, slow=slow, signal=signal, offset=offset)

    plt.subplot(211)
    plt.title(
        f"Moving Average Convergence Divergence (MACD) on {gst.instrument.ticker}"
    )
    if gst.instrument.interval == "1440min":
        plt.plot(
            gst.instrument.data.index,
            gst.instrument.data["5. adjusted close"].values,
            "k",
            lw=2,
        )
    else:
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["4. close"].values, "k", lw=2
        )
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.ylabel("Share Price ($)")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.subplot(212)
    plt.plot(df_ta.index, df_ta.iloc[:, 0].values, "b", lw=2)
    plt.plot(df_ta.index, df_ta.iloc[:, 2].values, "r", lw=2)
    plt.bar(df_ta.index, df_ta.iloc[:, 1].values, color="g")
    plt.legend(
        [
            f"MACD Line {df_ta.columns[0]}",
            f"Signal Line {df_ta.columns[2]}",
            f"Histogram {df_ta.columns[1]}",
        ]
    )
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.xlabel("Time")

    return fig


def rsi(
    gst: gamestonk_terminal.GamestonkTerminal,
    length: int,
    scalar: int,
    drift: int,
    offset: int,
):
    fig, _ = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.rsi(
        length=length,
        scalar=scalar,
        drift=drift,
        offset=offset,
    )

    plt.subplot(211)
    if gst.instrument.interval == "1440min":
        plt.plot(
            gst.instrument.data.index,
            gst.instrument.data["5. adjusted close"].values,
            "k",
            lw=2,
        )
    else:
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["4. close"].values, "k", lw=2
        )
    plt.title(f"Relative Strength Index (RSI) on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.ylabel("Share Price ($)")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.subplot(212)
    plt.plot(df_ta.index, df_ta.values, "b", lw=2)
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.axhspan(70, 100, facecolor="r", alpha=0.2)
    plt.axhspan(0, 30, facecolor="g", alpha=0.2)
    plt.axhline(70, linewidth=3, color="r", ls="--")
    plt.axhline(30, linewidth=3, color="g", ls="--")
    plt.xlabel("Time")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.ylim([0, 100])
    plt.gca().twinx()
    plt.ylim(plt.gca().get_ylim())
    plt.yticks([0.15, 0.85], ("OVERSOLD", "OVERBOUGHT"))

    return fig


def stoch(
    gst: gamestonk_terminal.GamestonkTerminal,
    fastkperiod: int,
    slowdperiod: int,
    slowkperiod: int,
    offset: int,
):
    fig, _ = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.stoch(
        fastkperiod=fastkperiod,
        slowdperiod=slowdperiod,
        slowkperiod=slowkperiod,
        offset=offset,
    )

    plt.figure(figsize=plot_autoscale(), dpi=PLOT_DPI)
    plt.subplot(211)
    if gst.instrument.interval == "1440min":
        plt.plot(
            gst.instrument.data.index,
            gst.instrument.data["5. adjusted close"].values,
            "k",
            lw=2,
        )
    else:
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["4. close"].values, "k", lw=2
        )
    plt.title(
        f"Stochastic Relative Strength Index (STOCH RSI) on {gst.instrument.ticker}"
    )
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.ylabel("Share Price ($)")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.subplot(212)
    plt.plot(df_ta.index, df_ta.iloc[:, 0].values, "k", lw=2)
    plt.plot(df_ta.index, df_ta.iloc[:, 1].values, "b", lw=2, ls="--")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.axhspan(80, 100, facecolor="r", alpha=0.2)
    plt.axhspan(0, 20, facecolor="g", alpha=0.2)
    plt.axhline(80, linewidth=3, color="r", ls="--")
    plt.axhline(20, linewidth=3, color="g", ls="--")
    plt.legend([f"%K {df_ta.columns[0]}", f"%D {df_ta.columns[1]}"])
    plt.xlabel("Time")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.ylim([0, 100])
    plt.gca().twinx()
    plt.ylim(plt.gca().get_ylim())
    plt.yticks([0.1, 0.9], ("OVERSOLD", "OVERBOUGHT"))

    return fig
