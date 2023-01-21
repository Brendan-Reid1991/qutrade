from contextlib import closing
import pandas as pd
import numpy as np
from datetime import date as dt
from plot_module import *
from abc import ABC


class GetInfo(ABC):
    def __init__(self, ticker: str, date: datetime.date = dt.today()):
        self.ticker = ticker
        self.date = date
        self.date_str = self.date.strftime("%d-%b-%Y")

        self.file = f"data/{self.date_str}/{self.ticker}"
        self.data = pd.read_csv(self.file)

    def close(self):
        return self.data["4. close"][0]

    def _closing_(self):
        closing_price = self.data["4. close"][::-1]
        L = len(closing_price)
        blank_prices = list(np.where(closing_price.isnull())[0])
        for r_ in blank_prices:
            closing_price[r_] = float(
                (closing_price[r_ - 1] + closing_price[r_ + 1]) / 2)
        return list(closing_price)

    def previous_week(self):
        return self.data[0:7]

    def rolling_average(self, range: int = 50):

        closing_price = self._closing_()

        rolling_average = []
        cum_price = 0
        for idx, price in enumerate(closing_price[0:range]):
            cum_price += price
            avg = cum_price / (idx+1)
            rolling_average.append(avg)

        i = 1
        end = 0
        while end < len(closing_price):
            start = 0 + i
            end = range + i
            r_a = sum(closing_price[start:end]) / range
            rolling_average.append(r_a)
            i += 1

        return rolling_average

    def analyse(self, years: int = 1):
        L = 52 * 5 * years

        closing_price = self._closing_()[-L::]
        volume_traded = self.data['5. volume'].tolist()[0:L][::-1]
        Dates = self.data['date'].tolist()[0:L][::-1]

        rolling_averages = [
            self.rolling_average(x)[-L::] for x in [50, 100, 200]
        ]

        plot_graph(self.file, Dates, closing_price,
                   volume_traded, rolling_averages, years=years)
