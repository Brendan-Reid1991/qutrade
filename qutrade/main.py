from get_data import GetData
from get_info import GetInfo
from scoring import Score
import os

str = "SUR.LON"


class StockChecker():
    def __init__(self, index: str):
        self.index = index
        data = GetData(self.index)
        if not os.path.exists(data.path()):
            data.download()

    def plot(self, years: int = 1):
        return GetInfo(self.index).analyse(years=years)

    @property
    def score(self):
        return Score(self.index)

    def past_week(self):
        return GetInfo(self.index).previous_week()

    def rolling_average(self, days: int = 50, show_all: bool = False):
        if show_all:
            return GetInfo(self.index).rolling_average(range=days)
        else:
            return (f"Rolling {days} day average is"
                    f" {GetInfo(self.index).rolling_average(range=days)[-1]:.2f}")

    @property
    def key_info(self):
        for days in [50, 200]:
            print(f"Rolling {days} day average is"
                    f" {GetInfo(self.index).rolling_average(range=days)[-1]:.2f}")
        print(f"Score is {self.score} out of 6")


stock = StockChecker("TEK.LON")

# stock.plot()
print(stock.past_week())
