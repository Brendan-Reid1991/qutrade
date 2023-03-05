from qutrade.investigate import TimeSeries
from qutrade.types import Ticker

ibm = TimeSeries(Ticker("IBM"))

data = ibm.intraday(save=True)

# print(data.index.get_level_values("date"))
