# IMPORTATION STANDARD
from datetime import datetime, timedelta

# IMPORTATION THIRDPARTY
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import yfinance as yf
import pytz


# IMPORTATION INTERNAL
from gamestonk_terminal.models.instrument import Instrument
import gamestonk_terminal.models.technical_analysis as ta
from gamestonk_terminal import config_terminal as cfg


class GamestonkTerminal:
    def __init__(
        self,
    ):
        self.cfg = cfg

        self.instrument = Instrument()

    def update_instrument(
        self,
        context: str,
        ticker: str,
        source: str,
        interval: int = 1440,
        prepost: bool = False,
        start: datetime = datetime.utcnow() - timedelta(days=365),
    ):

        if context == "stock":
            # Daily
            if interval == 1440:

                # Alpha Vantage Source
                if source == "av":
                    ts = TimeSeries(
                        key=self.cfg.API_KEY_ALPHAVANTAGE, output_format="pandas"
                    )
                    # pylint: disable=unbalanced-tuple-unpacking
                    df_stock_candidate, _ = ts.get_daily_adjusted(
                        symbol=ticker, outputsize="full"
                    )

                    # Check that loading a stock was not successful
                    if df_stock_candidate.empty:
                        return

                    # pylint: disable=no-member
                    df_stock_candidate.sort_index(ascending=True, inplace=True)

                    # Slice dataframe from the starting date YYYY-MM-DD selected
                    df_stock_candidate = df_stock_candidate[start:]

                    df_stock_candidate = df_stock_candidate.rename(
                        columns={
                            "1. open": "open",
                            "2. high": "high",
                            "3. low": "low",
                            "5. adjusted close": "close",
                            "6. volume": "volume",
                        },
                    )

                # Yahoo Finance Source
                elif source == "yf":
                    df_stock_candidate = yf.download(
                        ticker, start=start, progress=False
                    )

                    # Check that loading a stock was not successful
                    if df_stock_candidate.empty:
                        return

                    df_stock_candidate = df_stock_candidate.rename(
                        columns={
                            "Open": "open",
                            "High": "high",
                            "Low": "low",
                            "Adj Close": "close",
                            "Volume": "volume",
                        }
                    )
                    df_stock_candidate.index.name = "date"

                # Check if start time from dataframe is more recent than specified
                if df_stock_candidate.index[0] > pd.to_datetime(start):
                    s_start = df_stock_candidate.index[0]
                else:
                    s_start = start

            # Intraday
            else:

                # Alpha Vantage Source
                if source == "av":
                    ts = TimeSeries(
                        key=self.cfg.API_KEY_ALPHAVANTAGE, output_format="pandas"
                    )
                    # pylint: disable=unbalanced-tuple-unpacking
                    df_stock_candidate, _ = ts.get_intraday(
                        symbol=ticker,
                        outputsize="full",
                        interval=str(interval) + "min",
                    )

                    # Check that loading a stock was not successful
                    if df_stock_candidate.empty:
                        return

                    # pylint: disable=no-member
                    df_stock_candidate.sort_index(ascending=True, inplace=True)

                    # Slice dataframe from the starting date YYYY-MM-DD selected
                    df_stock_candidate = df_stock_candidate[start:]

                    # Check if start time from dataframe is more recent than specified
                    if df_stock_candidate.index[0] > pd.to_datetime(start):
                        s_start = df_stock_candidate.index[0]
                    else:
                        s_start = start

                    df_stock_candidate = df_stock_candidate.rename(
                        columns={
                            "1. open": "open",
                            "2. high": "high",
                            "3. low": "low",
                            "5. adjusted close": "close",
                            "6. volume": "volume",
                        },
                    )

                # Yahoo Finance Source
                elif source == "yf":
                    s_int = str(interval) + "m"

                    d_granularity = {
                        "1m": 6,
                        "5m": 59,
                        "15m": 59,
                        "30m": 59,
                        "60m": 729,
                    }

                    s_start_dt = datetime.utcnow() - timedelta(
                        days=d_granularity[s_int]
                    )
                    s_date_start = s_start_dt.strftime("%Y-%m-%d")

                    if s_start_dt > start:
                        # Using Yahoo Finance with granularity {s_int} the starting date is set to: {s_date_start}

                        df_stock_candidate = yf.download(
                            ticker,
                            start=s_date_start,
                            progress=False,
                            interval=s_int,
                            prepost=prepost,
                        )

                    else:
                        df_stock_candidate = yf.download(
                            ticker,
                            start=start.strftime("%Y-%m-%d"),
                            progress=False,
                            interval=s_int,
                            prepost=prepost,
                        )

                    # Check that loading a stock was not successful
                    if df_stock_candidate.empty:
                        return

                    if s_start_dt > start:
                        s_start = pytz.utc.localize(s_start_dt)
                    else:
                        s_start = start

                    df_stock_candidate = df_stock_candidate.rename(
                        columns={
                            "Open": "open",
                            "High": "high",
                            "Low": "low",
                            "Close": "close",
                            "Volume": "volume",
                        }
                    )
                    df_stock_candidate.index.name = "date"

            self.instrument.context = context
            self.instrument.ticker = ticker
            self.instrument.source = source
            self.instrument.interval = interval
            self.instrument.prepost = prepost
            self.instrument.start = s_start
            self.instrument.data = df_stock_candidate

            self.ta = ta.TechnicalAnalysis(instrument=self.instrument)

        else:
            print("Unavailable context")
