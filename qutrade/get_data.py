from datetime import date
import pandas as pd
import os
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData


class GetData:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.api = open("AVAPI.txt", "r").readlines()[0]

        if self.ticker[-3:] != "LON":
            raise ValueError(
                "Tickers for LSE should end in .LON - "
                "are you sure the entered ticker is correct?"
            )

    def today(self):
        return date.today().strftime("%d-%b-%Y")

    def path(self):
        destination = f"data/{self.today()}"
        if not os.path.isdir(destination):
            os.makedirs(destination, exist_ok=True)

        filename = destination + f"/{self.ticker}"
        return filename

    def download(self):
        ts = TimeSeries(self.api, output_format="pandas")
        data, meta_data = ts.get_daily(self.ticker, outputsize="full")
        data.to_csv(self.path())

    def load(self):
        df = pd.read_csv(self.path)
        return df


class get_fundamentals:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.api = open("AVAPI.txt", "r").readlines()[0]

    @classmethod
    def eps(self):
        FundamentalData.get_company_overview(self.ticker)
