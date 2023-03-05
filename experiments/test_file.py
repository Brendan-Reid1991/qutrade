from qutrade.investigate import Inspect
from qutrade.types import Ticker

ibm = Inspect(Ticker("IBM"))

data = ibm.intraday(save=True)

# print(data.index.get_level_values("date"))
