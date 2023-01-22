from __future__ import annotations
from typing import Optional
import os
import warnings

from alpha_vantage.timeseries import TimeSeries

from qutrade.types import Ticker, api

ACCESS_KEY = api()


def output_warning(arg: str):
    warnings.warn(
        f"Output type specified incorrectly: {arg}. Must be on of 'compact' or 'full', defaulting to 'full'.")


class Inspect:
    def __init__(self, ticker: Ticker):
        self.ticker = ticker
        self.pathway = f'qutrade/data/{self.ticker}/'
        self._time_series = TimeSeries(ACCESS_KEY, output_format='pandas')
        if not os.path.exists(self.pathway):
            os.makedirs(self.pathway)

    def intraday(self, interval: int = 60, output: str = 'full'):
        """Get the intraday data and save it to a CSV file.

        Parameters
        ----------
        interval : int, optional
            Time interval between two consecutive data points in the time series
            in units of minutes, by default 60. Accepted values are 1, 5, 15, 30 or 60.
        output : str, optional
            How much data to take, accepted values are 'compact' or 'full'.
            By default None

        Raises
        ------
        ValueError
            If interval is not an accepted value.

        Warning
            If the output type is not one of 'compact' or 'full', defaults to 'full'.
        """
        if interval not in [1, 5, 15, 30, 60]:
            raise ValueError(
                f"Incorrect interval value given: {interval}."
                " Must be one of 1, 5, 15, 30 or 60 (minutes).")
        output = "full" if output is None else output
        if output not in ["compact", "full"]:
            output_warning(output)
            output = 'full'

        data, metadata = self._time_series.get_intraday(
            self.ticker, outputsize=output)
        data.to_csv(self.pathway+f"/{self.ticker}_Intraday", index=False)

    def daily(self, output: str = 'full'):
        """Get the daily data and save it to a CSV file. Requires premium API.

        Parameters
        ----------
        output : str, optional
            How much data to take, accepted values are 'compact' or 'full'.
            By default None

        Raises
        ------
        ValueError
            If interval is not an accepted value.

        Warning
            If the output type is not one of 'compact' or 'full', defaults to 'full'.
        """
        output = "full" if output is None else output
        if output not in ["compact", "full"]:
            output_warning(output)
            output = 'full'

        data, metadata = self._time_series.get_intraday(
            self.ticker, outputsize=output)
        data.to_csv(self.pathway+f"/{self.ticker}_Intraday", index=False)
