import pytest
import warnings

import pandas as pd

from qutrade.investigate._inspector import output_warning
from qutrade.investigate import Inspect
from qutrade.types import Ticker


@pytest.mark.parametrize("arg", ["X", 4, "aaaaa"])
def test_output_warning(arg):
    with pytest.warns(
        UserWarning,
        match=f"Output type specified incorrectly: {arg}. Must be on of 'compact' or 'full', defaulting to 'full'.",
    ):
        output_warning(arg)


class TestInspect:
    @pytest.mark.parametrize("ticker", ["IBM", "GOOG", "MSFT"])
    def test_init(self, ticker):
        ticker = Ticker(ticker)
        inspect = Inspect(ticker)
        assert inspect.ticker == ticker
        assert inspect.pathway == f"data/{ticker}/"

    @pytest.fixture(scope="class")
    def IBM(self):
        return Inspect(Ticker("IBM"))

    def test_intraday_return_type(self, IBM):
        assert isinstance(IBM.intraday(), pd.DataFrame)

    @pytest.mark.parametrize("interval", list(range(0, 100)))
    def test_intraday_interval_error(self, IBM, interval):
        if interval not in [1, 5, 15, 30, 60]:
            with pytest.raises(ValueError, match="Incorrect interval value given"):
                IBM.intraday(interval=interval)

    def test_intraday_output_warning(self, IBM):
        with pytest.warns(UserWarning):
            IBM.intraday(output="blarg")

    def test_daily_adjusted_return_type(self, IBM):
        assert isinstance(IBM.daily(adjusted=True), pd.DataFrame)

    def test_daily_adjusted_csv_headers(self, IBM):
        assert any("adjusted" in x for x in IBM.daily(adjusted=True).columns)

    @pytest.mark.xfail()
    def test_daily_unadjusted_return_type(self, IBM):
        assert isinstance(IBM.daily(adjusted=False), pd.DataFrame)

    @pytest.mark.xfail()
    def test_daily_unadjusted_csv_headers(self, IBM):
        assert any("adjusted" in x for x in IBM.daily(adjusted=False).columns)

    def test_weekly_adjusted_return_type(self, IBM):
        assert isinstance(IBM.weekly(adjusted=True), pd.DataFrame)

    def test_weekly_adjusted_csv_headers(self, IBM):
        assert any("adjusted" in x for x in IBM.weekly(adjusted=True).columns)

    @pytest.mark.xfail()
    def test_weekly_unadjusted_return_type(self, IBM):
        assert isinstance(IBM.weekly(adjusted=False), pd.DataFrame)

    @pytest.mark.xfail()
    def test_weekly_unadjusted_csv_headers(self, IBM):
        assert any("adjusted" in x for x in IBM.weekly(adjusted=False).columns)
