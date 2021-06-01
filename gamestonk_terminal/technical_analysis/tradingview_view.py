from gamestonk_terminal.models import gamestonk_terminal


def print_recommendation(
    gst: gamestonk_terminal.GamestonkTerminal,
    screener: str,
    exchange: str,
    interval: str,
):
    """Print tradingview recommendation based on technical indicators

    Parameters
    ----------
    other_args : List[str]
        Command line arguments to be processed with argparse
    ticker : str
        Ticker to get tradingview recommendation based on technical indicators
    """
    return gst.ta.tradingview_recommendation(screener, exchange, interval)
