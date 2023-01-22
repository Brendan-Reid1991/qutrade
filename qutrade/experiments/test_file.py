from qutrade.investigate import Inspect
from qutrade.types import Ticker

fourd_pharma = Inspect(Ticker("IBM"))

fourd_pharma.intraday()
