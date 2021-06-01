import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from gamestonk_terminal.helper_funcs import (
    plot_autoscale,
)
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.models import gamestonk_terminal

register_matplotlib_converters()


def plot_adx(
    gst: gamestonk_terminal.GamestonkTerminal,
    length: int,
    scalar: int,
    drift: int,
    offset: int,
):
    fig = plt.figure(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.adx(
        length=length,
        scalar=scalar,
        drift=drift,
        offset=offset,
    )

    plt.subplot(211)
    plt.plot(gst.instrument.data.index, gst.instrument.data["close"].values, "k", lw=2)
    plt.title(f"Average Directional Movement Index (ADX) on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.ylabel("Share Price ($)")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.subplot(212)
    plt.plot(df_ta.index, df_ta.iloc[:, 0].values, "b", lw=2)
    plt.plot(df_ta.index, df_ta.iloc[:, 1].values, "g", lw=1)
    plt.plot(df_ta.index, df_ta.iloc[:, 2].values, "r", lw=1)
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.axhline(25, linewidth=3, color="k", ls="--")
    plt.legend(
        [
            f"ADX ({df_ta.columns[0]})",
            f"+DI ({df_ta.columns[1]})",
            f"- DI ({df_ta.columns[2]})",
        ]
    )
    plt.xlabel("Time")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.ylim([0, 100])

    return fig


def plot_aroon(
    gst: gamestonk_terminal.GamestonkTerminal,
    length: int,
    scalar: int,
    offset: int,
):
    fig = plt.figure(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.aroon(
        length=length,
        scalar=scalar,
        offset=offset,
    )

    plt.subplot(311)
    # Daily
    if gst.instrument.interval == "1440min":
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["close"].values, "k", lw=2
        )
    # Intraday
    else:
        plt.plot(
            gst.instrument.data.index, gst.instrument.data["close"].values, "k", lw=2
        )

    plt.title(f"Aroon on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.ylabel("Share Price ($)")
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)

    plt.subplot(312)
    plt.plot(df_ta.index, df_ta.iloc[:, 0].values, "r", lw=2)
    plt.plot(df_ta.index, df_ta.iloc[:, 1].values, "g", lw=2)
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.axhline(50, linewidth=1, color="k", ls="--")
    plt.legend([f"Aroon DOWN ({df_ta.columns[0]})", f"Aroon UP ({df_ta.columns[1]})"])
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.ylim([0, 100])

    plt.subplot(313)
    plt.plot(df_ta.index, df_ta.iloc[:, 2].values, "b", lw=2)
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.xlabel("Time")
    plt.legend([f"Aroon OSC ({df_ta.columns[2]})"])
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
    plt.ylim([-100, 100])

    return fig
