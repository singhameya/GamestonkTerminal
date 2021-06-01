""" Finviz View """
__docformat__ = "numpy"

import io
import requests
import matplotlib.pyplot as plt
from finvizfinance.quote import finvizfinance
from finvizfinance.util import headers
from PIL import Image

from gamestonk_terminal.helper_funcs import (
    plot_autoscale,
)
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.models import gamestonk_terminal


def view(gst: gamestonk_terminal.GamestonkTerminal):
    """View historical price with trendlines. [Source: Finviz]

    Parameters
    ----------
    other_args : List[str]
        argparse other args
    ticker: str
        stock ticker
    """
    stock = finvizfinance(gst.instrument.ticker)
    image_url = stock.TickerCharts(urlonly=True)

    r = requests.get(image_url, stream=True, headers=headers, timeout=5)
    r.raise_for_status()
    r.raw.decode_content = True

    dataBytesIO = io.BytesIO(r.content)
    im = Image.open(dataBytesIO)

    fig, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    ax.set_axis_off()
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    plt.imshow(im)

    return fig
