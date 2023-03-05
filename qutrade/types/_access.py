from typing import Optional, NewType
from pathlib import Path

Ticker = NewType("Ticker", str)


def api(path: Optional[Path] = None) -> str:
    """Access your unique API key for alpha_vantage.

    Parameters
    ----------
    path : Optional[Path], optional
        The pathlib.Path directory where the key file is stored, by default None.
        If None, the parent directory (`../qutrade`) is accessed with filename `key.txt.`

    Returns
    -------
    str
        Your unique API key.
    """
    if path is None:
        return open("key.txt", "r").read().strip()
    return open(path, "rb").read().strip()
