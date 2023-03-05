from __future__ import annotations
import os
import warnings

import pandas as pd
from alpha_vantage.timeseries import TimeSeries

from qutrade.types import Ticker, api

ACCESS_KEY = api()


def output_warning(arg: str):
    warnings.warn(
        f"Output type specified incorrectly: {arg}."
        " Must be on of 'compact' or 'full', defaulting to 'full'."
    )


class Inspect:
    def __init__(self, ticker: Ticker):
        self.ticker = ticker
        self.pathway = f"qutrade/data/{self.ticker}/"
        self._time_series = TimeSeries(ACCESS_KEY, output_format="pandas")
        if not os.path.exists(self.pathway):
            os.makedirs(self.pathway)

    def intraday(
        self, interval: int = 60, output: str = "full", save: bool = False
    ) -> pd.DataFrame:
        """Get the intraday data for the given ticker.

        Parameters
        ----------
        interval : int, optional
            Time interval between two consecutive data points in the time series
            in units of minutes, by default 60. Accepted values are 1, 5, 15, 30 or 60.
        output : str, optional
            How much data to take, accepted values are 'compact' or 'full'.
            By default None
        save : bool, optional
            Whether or not to save the data to a CSV, by default False.

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
                " Must be one of 1, 5, 15, 30 or 60 (minutes)."
            )
        output = "full" if output is None else output
        if output not in ["compact", "full"]:
            output_warning(output)
            output = "full"

        data, _ = self._time_series.get_intraday(self.ticker, outputsize=output)
        data = data.reset_index()
        if save:
            data.to_csv(self.pathway + f"/{self.ticker}_Intraday.csv", index=False)

        return data

    def daily(
        self, adjusted: bool = True, output: str = "full", save: bool = False
    ) -> pd.DataFrame:
        """Get the daily data.
        Unadjusted data requires a premium API.

        Parameters
        ----------
        adjsuted : bool, optional
            Whether or not to access the adjusted daily data.
        output : str, optional
            How much data to take, accepted values are 'compact' or 'full'.
            By default None
        save : bool, optional
            Whether or not to save the data to a CSV, by default False.

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
            output = "full"

        if adjusted:
            data, _ = self._time_series.get_daily_adjusted(
                self.ticker, outputsize=output
            )
        else:
            data, _ = self._time_series.get_daily(self.ticker, outputsize=output)

        data = data.reset_index()

        suffix = "" if not adjusted else "Adjusted"
        if save:
            data.to_csv(self.pathway + f"/{self.ticker}_Daily{suffix}", index=False)

        return data

    def weekly(self, adjusted: bool = True, save: bool = False) -> pd.DataFrame:
        """Get the weekly data and save it to a CSV file.

        Parameters
        ----------
        adjusted : bool, optional
            Whether or not to access the adjusted daily data.
        save : bool, optional
            Whether or not to save the data to a CSV, by default False.

        Raises
        ------
        ValueError
            If interval is not an accepted value.

        Warning
            If the output type is not one of 'compact' or 'full', defaults to 'full'.
        """
        if adjusted:
            data, _ = self._time_series.get_weekly_adjusted(self.ticker)
        else:
            data, _ = self._time_series.get_weekly(self.ticker)
        data = data.reset_index()
        suffix = "" if not adjusted else "Adjusted"
        data.to_csv(self.pathway + f"/{self.ticker}_Weekly{suffix}", index=False)

        return data

    def monthly(self, adjusted: bool = True, save: bool = False):
        """Get the monthly data and save it to a CSV file.

        Parameters
        ----------
        adjusted : bool, optional
            Whether or not to access the adjusted daily data.

        Raises
        ------
        ValueError
            If interval is not an accepted value.

        Warning
            If the output type is not one of 'compact' or 'full', defaults to 'full'.
        """

        if adjusted:
            data, _ = self._time_series.get_monthly_adjusted(self.ticker)
        else:
            data, _ = self._time_series.get_monthly(self.ticker)
        data = data.reset_index()
        suffix = "" if not adjusted else "Adjusted"
        data.to_csv(self.pathway + f"/{self.ticker}_Monthly{suffix}", index=False)

        return data
