import pytest
import warnings

from qutrade.investigate._inspector import output_warning
from qutrade.investigate import Inspect
from qutrade.types import Ticker


@pytest.mark.parametrize("arg", ["X", 4, "aaaaa"])
def test_output_warning(arg):
    with pytest.warns(UserWarning, match=f"Output type specified incorrectly: {arg}. Must be on of 'compact' or 'full', defaulting to 'full'."):
        output_warning(arg)


class TestInspect:
    @pytest.mark.parametrize("ticker", ["IBM", "GOOG", "MSFT"])
    def test_init(self, ticker):
        ticker = Ticker(ticker)
        inspect = Inspect(ticker)
        assert inspect.ticker == ticker
        assert inspect.pathway == f"qutrade/data/{ticker}/"
