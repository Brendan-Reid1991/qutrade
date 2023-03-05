import pytest
from pathlib import Path

from qutrade.types import api, Ticker


class TestAPI:
    def test_default_pathway_returns_str(self):
        assert isinstance(api(), str)

    # def test_no_filetype_returns_str(self):
    #     assert isinstance(api(Path('key')), str)

    # def test_pkl_returns_str(self):
    #     assert isinstance(api(Path('key.pkl')), str)
