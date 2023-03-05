from qutrade.investigate import DataHandler
from qutrade.types import Ticker

ibm = DataHandler(Ticker("IBM"))

data = ibm.intraday(save=True)

# print(data.index.get_level_values("date"))
