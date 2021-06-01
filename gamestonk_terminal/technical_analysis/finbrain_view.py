from gamestonk_terminal.models import gamestonk_terminal


def technical_report(gst: gamestonk_terminal.GamestonkTerminal):
    """Print technical summary report provided by FinBrain's API

    Parameters
    ----------
    other_args : List[str]
        Command line arguments to be processed with argparse
    ticker : str
        Ticker to get the technical summary
    """
    return gst.ta.finbrain_technical_report()
