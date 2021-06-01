"""Technical Analysis Controller Module"""
__docformat__ = "numpy"

import argparse
import os
from typing import List
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from prompt_toolkit.completion import NestedCompleter

from gamestonk_terminal.helper_funcs import (
    check_positive,
    parse_known_args_and_warn,
)

from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.helper_funcs import get_flair
from gamestonk_terminal.menu import session
from gamestonk_terminal.technical_analysis import momentum_view
from gamestonk_terminal.technical_analysis import overlap_view
from gamestonk_terminal.technical_analysis import trend_view
from gamestonk_terminal.technical_analysis import volatility_view
from gamestonk_terminal.technical_analysis import volume_view
from gamestonk_terminal.technical_analysis import finbrain_view
from gamestonk_terminal.technical_analysis import tradingview_view
from gamestonk_terminal.technical_analysis import finviz_view
from gamestonk_terminal.technical_analysis import finnhub_view


class TechnicalAnalysisController:
    """Technical Analysis Controller class"""

    # Command choices
    CHOICES = [
        "help",
        "q",
        "quit",
        "view",
        "summary",
        "recom",
        "pr",
        "ema",
        "sma",
        "vwap",
        "cci",
        "macd",
        "rsi",
        "stoch",
        "adx",
        "aroon",
        "bbands",
        "ad",
        "obv",
    ]

    def __init__(
        self,
        stock: pd.DataFrame,
        ticker: str,
        start: datetime,
        interval: str,
        gst,
    ):
        """Constructor"""
        self.stock = stock
        self.ticker = ticker
        self.start = start
        self.interval = interval
        self.delete_img = False
        self.gst = gst
        self.ta_parser = argparse.ArgumentParser(add_help=False, prog="ta")
        self.ta_parser.add_argument(
            "cmd",
            choices=self.CHOICES,
        )

    def print_help(self):
        """Print help"""

        s_intraday = (f"Intraday {self.interval }", "Daily")[self.interval == "1440min"]

        if self.start:
            print(
                f"\n{s_intraday} Stock: {self.ticker} (from {self.start.strftime('%Y-%m-%d')})"
            )
        else:
            print(f"\n{s_intraday} Stock: {self.ticker}")

        print("\nTechnical Analysis:")  # https://github.com/twopirllc/pandas-ta
        print("   help        show this technical analysis menu again")
        print("   q           quit this menu, and shows back to main menu")
        print("   quit        quit to abandon program")
        print("")
        print("   view        view historical data and trendlines [Finviz]")
        print("   summary     technical summary report [FinBrain API]")
        print(
            "   recom       recommendation based on Technical Indicators [Tradingview API]"
        )
        print("   pr          pattern recognition [Finnhub]")
        print("")
        print("overlap:")
        print("   ema         exponential moving average")
        print("   sma         simple moving average")
        print("   vwap        volume weighted average price")
        print("momentum:")
        print("   cci         commodity channel index")
        print("   macd        moving average convergence/divergence")
        print("   rsi         relative strength index")
        print("   stoch       stochastic oscillator")
        print("trend:")
        print("   adx         average directional movement index")
        print("   aroon       aroon indicator")
        print("volatility:")
        print("   bbands      bollinger bands")
        print("volume:")
        print("   ad          chaikin accumulation/distribution line values")
        print("   obv         on balance volume")
        print("")

    def switch(self, an_input: str):
        """Process and dispatch input

        Returns
        -------
        True, False or None
            False - quit the menu
            True - quit the program
            None - continue in the menu
        """

        (known_args, other_args) = self.ta_parser.parse_known_args(an_input.split())

        # Due to Finviz implementation of Spectrum, we delete the generated spectrum figure
        # after saving it and displaying it to the user
        if self.delete_img:
            # Confirm that file exists
            if os.path.isfile(self.ticker + ".jpg"):
                os.remove(self.ticker + ".jpg")
                self.delete_img = False

        return getattr(
            self, "call_" + known_args.cmd, lambda: "Command not recognized!"
        )(other_args)

    def call_help(self, _):
        """Process Help command"""
        self.print_help()

    def call_q(self, _):
        """Process Q command - quit the menu"""
        return False

    def call_quit(self, _):
        """Process Quit command - quit the program"""
        return True

    def call_view(self, other_args: List[str]):
        """Process view command"""
        finviz_view.view(other_args, self.ticker)
        self.delete_img = True

    def call_summary(self, other_args: List[str]):
        """Process summary command"""
        finbrain_view.technical_summary_report(other_args, self.ticker)

    def call_recom(self, other_args: List[str]):
        """Process recom command"""
        tradingview_view.print_recommendation(other_args, self.ticker)

    def call_pr(self, other_args: List[str]):
        """Process pr command"""
        finnhub_view.pattern_recognition_view(other_args, self.ticker)

    # OVERLAP
    def call_ema(self, other_args: List[str]):
        """Process ema command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="ema",
            description="""
            The Exponential Moving Average is a staple of technical
            analysis and is used in countless technical indicators. In a Simple Moving
            Average, each value in the time period carries equal weight, and values outside
            of the time period are not included in the average. However, the Exponential
            Moving Average is a cumulative calculation, including all data. Past values have
            a diminishing contribution to the average, while more recent values have a greater
            contribution. This method allows the moving average to be more responsive to changes
            in the data.
        """,
        )
        parser.add_argument(
            "-l",
            "--length",
            dest="length",
            type=lambda s: [int(item) for item in s.split(",")],
            default=[20, 50],
            help="length of MA window",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = overlap_view.plot_ema(self.gst, ns_parser.length, ns_parser.offset)

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    def call_sma(self, other_args: List[str]):
        """Process sma command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="sma",
            description="""
                Moving Averages are used to smooth the data in an array to
                help eliminate noise and identify trends. The Simple Moving Average is literally
                the simplest form of a moving average. Each output value is the average of the
                previous n values. In a Simple Moving Average, each value in the time period carries
                equal weight, and values outside of the time period are not included in the average.
                This makes it less responsive to recent changes in the data, which can be useful for
                filtering out those changes.
            """,
        )
        parser.add_argument(
            "-l",
            "--length",
            dest="length",
            type=lambda s: [int(item) for item in s.split(",")],
            default=[20, 50],
            help="length of MA window",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = overlap_view.plot_sma(self.gst, ns_parser.length, ns_parser.offset)

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    def call_vwap(self, other_args: List[str]):
        """Process vwap command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="vwap",
            description="""
                The Volume Weighted Average Price that measures the average typical price
                by volume. It is typically used with intraday charts to identify general direction.
            """,
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = overlap_view.plot_vwap(self.gst, ns_parser.offset)

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    # MOMENTUM
    def call_cci(self, other_args: List[str]):
        """Process cci command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="cci",
            description="""
                The CCI is designed to detect beginning and ending market trends.
                The range of 100 to -100 is the normal trading range. CCI values outside of this
                range indicate overbought or oversold conditions. You can also look for price
                divergence in the CCI. If the price is making new highs, and the CCI is not,
                then a price correction is likely.
            """,
        )
        parser.add_argument(
            "-l",
            "--length",
            action="store",
            dest="length",
            type=check_positive,
            default=14,
            help="length",
        )
        parser.add_argument(
            "-s",
            "--scalar",
            action="store",
            dest="scalar",
            type=check_positive,
            default=0.015,
            help="scalar",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )
        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = momentum_view.plot_cci(
                self.gst, ns_parser.length, ns_parser.scalar, ns_parser.offset
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    def call_macd(self, other_args: List[str]):
        """Process macd command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="macd",
            description="""
                The Moving Average Convergence Divergence (MACD) is the difference
                between two Exponential Moving Averages. The Signal line is an Exponential Moving
                Average of the MACD. \n \n The MACD signals trend changes and indicates the start
                of new trend direction. High values indicate overbought conditions, low values
                indicate oversold conditions. Divergence with the price indicates an end to the
                current trend, especially if the MACD is at extreme high or low values. When the MACD
                line crosses above the signal line a buy signal is generated. When the MACD crosses
                below the signal line a sell signal is generated. To confirm the signal, the MACD
                should be above zero for a buy, and below zero for a sell.
            """,
        )
        parser.add_argument(
            "-f",
            "--fast",
            action="store",
            dest="fast",
            type=check_positive,
            default=12,
            help="The short period.",
        )
        parser.add_argument(
            "-s",
            "--slow",
            action="store",
            dest="slow",
            type=check_positive,
            default=26,
            help="The long period.",
        )
        parser.add_argument(
            "--signal",
            action="store",
            dest="signal",
            type=check_positive,
            default=9,
            help="The signal period.",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="How many periods to offset the result.",
        )
        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = momentum_view.plot_macd(
                self.gst,
                ns_parser.fast,
                ns_parser.slow,
                ns_parser.signal,
                ns_parser.offset,
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    def call_rsi(self, other_args: List[str]):
        """Process rsi command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="rsi",
            description="""
                The Relative Strength Index (RSI) calculates a ratio of the
                recent upward price movements to the absolute price movement. The RSI ranges
                from 0 to 100. The RSI is interpreted as an overbought/oversold indicator when
                the value is over 70/below 30. You can also look for divergence with price. If
                the price is making new highs/lows, and the RSI is not, it indicates a reversal.
            """,
        )
        parser.add_argument(
            "-l",
            "--length",
            action="store",
            dest="length",
            type=check_positive,
            default=14,
            help="length",
        )
        parser.add_argument(
            "-s",
            "--scalar",
            action="store",
            dest="scalar",
            type=check_positive,
            default=100,
            help="scalar",
        )
        parser.add_argument(
            "-d",
            "--drift",
            action="store",
            dest="drift",
            type=check_positive,
            default=1,
            help="drift",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = momentum_view.plot_rsi(
                self.gst,
                ns_parser.length,
                ns_parser.scalar,
                ns_parser.drift,
                ns_parser.offset,
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    def call_stoch(self, other_args: List[str]):
        """Process stoch command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="stoch",
            description="""
                The Stochastic Oscillator measures where the close is in relation
                to the recent trading range. The values range from zero to 100. %D values over 75
                indicate an overbought condition; values under 25 indicate an oversold condition.
                When the Fast %D crosses above the Slow %D, it is a buy signal; when it crosses
                below, it is a sell signal. The Raw %K is generally considered too erratic to use
                for crossover signals.
            """,
        )
        parser.add_argument(
            "-k",
            "--fastkperiod",
            action="store",
            dest="fastkperiod",
            type=check_positive,
            default=14,
            help="The time period of the fastk moving average",
        )
        parser.add_argument(
            "-d",
            "--slowdperiod",
            action="store",
            dest="slowdperiod",
            type=check_positive,
            default=3,
            help="The time period of the slowd moving average",
        )
        parser.add_argument(
            "--slowkperiod",
            action="store",
            dest="slowkperiod",
            type=check_positive,
            default=3,
            help="The time period of the slowk moving average",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = momentum_view.plot_stoch(
                self.gst,
                ns_parser.fastkperiod,
                ns_parser.slowdperiod,
                ns_parser.slowkperiod,
                ns_parser.offset,
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    # TREND
    def call_adx(self, other_args: List[str]):
        """Process adx command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="adx",
            description="""
                The ADX is a Welles Wilder style moving average of the Directional Movement Index (DX).
                The values range from 0 to 100, but rarely get above 60. To interpret the ADX, consider
                a high number to be a strong trend, and a low number, a weak trend.
            """,
        )
        parser.add_argument(
            "-l",
            "--length",
            action="store",
            dest="length",
            type=check_positive,
            default=14,
            help="length",
        )
        parser.add_argument(
            "-s",
            "--scalar",
            action="store",
            dest="scalar",
            type=check_positive,
            default=100,
            help="scalar",
        )
        parser.add_argument(
            "-d",
            "--drift",
            action="store",
            dest="drift",
            type=check_positive,
            default=1,
            help="drift",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = trend_view.plot_adx(
                self.gst,
                ns_parser.length,
                ns_parser.scalar,
                ns_parser.drift,
                ns_parser.offset,
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    def call_aroon(self, other_args: List[str]):
        """Process aroon command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="aroon",
            description="""
                The word aroon is Sanskrit for "dawn's early light." The Aroon
                indicator attempts to show when a new trend is dawning. The indicator consists
                of two lines (Up and Down) that measure how long it has been since the highest
                high/lowest low has occurred within an n period range. \n \n When the Aroon Up is
                staying between 70 and 100 then it indicates an upward trend. When the Aroon Down
                is staying between 70 and 100 then it indicates an downward trend. A strong upward
                trend is indicated when the Aroon Up is above 70 while the Aroon Down is below 30.
                Likewise, a strong downward trend is indicated when the Aroon Down is above 70 while
                the Aroon Up is below 30. Also look for crossovers. When the Aroon Down crosses above
                the Aroon Up, it indicates a weakening of the upward trend (and vice versa).
            """,
        )
        parser.add_argument(
            "-l",
            "--length",
            action="store",
            dest="length",
            type=check_positive,
            default=25,
            help="length",
        )
        parser.add_argument(
            "-s",
            "--scalar",
            action="store",
            dest="scalar",
            type=check_positive,
            default=100,
            help="scalar",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = trend_view.plot_aroon(
                self.gst,
                ns_parser.length,
                ns_parser.scalar,
                ns_parser.offset,
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    # VOLATILITY
    def call_bbands(self, other_args: List[str]):
        """Process bbands command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="bbands",
            description="""
                Bollinger Bands consist of three lines. The middle band is a simple
                moving average (generally 20 periods) of the typical price (TP). The upper and lower
                bands are F standard deviations (generally 2) above and below the middle band.
                The bands widen and narrow when the volatility of the price is higher or lower,
                respectively. \n \nBollinger Bands do not, in themselves, generate buy or sell signals;
                they are an indicator of overbought or oversold conditions. When the price is near the
                upper or lower band it indicates that a reversal may be imminent. The middle band
                becomes a support or resistance level. The upper and lower bands can also be
                interpreted as price targets. When the price bounces off of the lower band and crosses
                the middle band, then the upper band becomes the price target.
            """,
        )
        parser.add_argument(
            "-l",
            "--length",
            action="store",
            dest="length",
            type=check_positive,
            default=5,
            help="length",
        )
        parser.add_argument(
            "-s",
            "--std",
            action="store",
            dest="std",
            type=check_positive,
            default=2,
            help="std",
        )
        parser.add_argument(
            "-m",
            "--mamode",
            action="store",
            dest="mamode",
            type=str,
            default="sma",
            help="mamode",
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = volatility_view.plot_bbands(
                self.gst,
                ns_parser.length,
                ns_parser.std,
                ns_parser.mamode,
                ns_parser.offset,
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    # VOLUME
    def call_ad(self, other_args: List[str]):
        """Process ad command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="ad",
            description="""
                The Accumulation/Distribution Line is similar to the On Balance
                Volume (OBV), which sums the volume times +1/-1 based on whether the close is
                higher than the previous close. The Accumulation/Distribution indicator, however
                multiplies the volume by the close location value (CLV). The CLV is based on the
                movement of the issue within a single bar and can be +1, -1 or zero. \n \n
                The Accumulation/Distribution Line is interpreted by looking for a divergence in
                the direction of the indicator relative to price. If the Accumulation/Distribution
                Line is trending upward it indicates that the price may follow. Also, if the
                Accumulation/Distribution Line becomes flat while the price is still rising (or falling)
                then it signals an impending flattening of the price.
            """,
        )

        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )
        parser.add_argument(
            "--open",
            action="store_true",
            default=False,
            dest="use_open",
            help="uses open value of stock",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = volume_view.plot_ad(
                self.gst,
                ns_parser.offset,
                ns_parser.use_open,
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")

    def call_obv(self, other_args: List[str]):
        """Process obv command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="obv",
            description="""
                The On Balance Volume (OBV) is a cumulative total of the up and
                down volume. When the close is higher than the previous close, the volume is added
                to the running total, and when the close is lower than the previous close, the volume
                is subtracted from the running total. \n \n To interpret the OBV, look for the OBV
                to move with the price or precede price moves. If the price moves before the OBV,
                then it is a non-confirmed move. A series of rising peaks, or falling troughs, in the
                OBV indicates a strong trend. If the OBV is flat, then the market is not trending.
            """,
        )
        parser.add_argument(
            "-o",
            "--offset",
            action="store",
            dest="offset",
            type=check_positive,
            default=0,
            help="offset",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            _ = volume_view.plot_obv(
                self.gst,
                ns_parser.offset,
            )

            if gtff.USE_ION:
                plt.ion()

            plt.show()
            print("")

        except Exception as e:
            print(e, "\n")


def menu(stock: pd.DataFrame, ticker: str, start: datetime, interval: str, gst=None):
    """Technical Analysis Menu"""

    ta_controller = TechnicalAnalysisController(stock, ticker, start, interval, gst)
    ta_controller.call_help(None)

    while True:
        # Get input command from user
        if session and gtff.USE_PROMPT_TOOLKIT:
            completer = NestedCompleter.from_nested_dict(
                {c: None for c in ta_controller.CHOICES}
            )
            an_input = session.prompt(
                f"{get_flair()} (ta)> ",
                completer=completer,
            )
        else:
            an_input = input(f"{get_flair()} (ta)> ")

        try:
            plt.close("all")

            process_input = ta_controller.switch(an_input)

            if process_input is not None:
                return process_input

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue
