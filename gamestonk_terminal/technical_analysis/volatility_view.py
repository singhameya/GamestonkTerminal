import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from gamestonk_terminal.helper_funcs import (
    plot_autoscale,
)
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.models import gamestonk_terminal

register_matplotlib_converters()


def plot_bbands(
    gst: gamestonk_terminal.GamestonkTerminal,
    length: int,
    std: int,
    mamode: str,
    offset: int,
):
    fig = plt.figure(figsize=plot_autoscale(), dpi=PLOT_DPI)

    df_ta = gst.ta.bbands(
        length=length,
        std=std,
        mamode=mamode,
        offset=offset,
    )

    plt.plot(
        gst.instrument.data.index, gst.instrument.data["close"].values, color="k", lw=3
    )
    plt.plot(df_ta.index, df_ta.iloc[:, 0].values, "r", lw=2)
    plt.plot(df_ta.index, df_ta.iloc[:, 1].values, "b", lw=1.5, ls="--")
    plt.plot(df_ta.index, df_ta.iloc[:, 2].values, "g", lw=2)
    plt.title(f"Bollinger Band (BBands) on {gst.instrument.ticker}")
    plt.xlim(gst.instrument.data.index[0], gst.instrument.data.index[-1])
    plt.xlabel("Time")
    plt.ylabel("Share Price ($)")
    plt.legend(
        [gst.instrument.ticker, df_ta.columns[0], df_ta.columns[1], df_ta.columns[2]]
    )
    plt.gca().fill_between(
        df_ta.index,
        df_ta.iloc[:, 0].values,
        df_ta.iloc[:, 2].values,
        alpha=0.1,
        color="b",
    )
    plt.grid(b=True, which="major", color="#666666", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)

    return fig
