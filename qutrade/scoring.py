import numpy as np
from datetime import date as dt
import pandas as pd
import ast


def transpose(L):
    return(list(map(list, zip(*L))))


def Score(ticker: str) -> int:
    close = "4. close"
    date_str = dt.today().strftime("%d-%b-%Y")
    df = pd.read_csv(f"data/{date_str}/{ticker}")
    One_Year_Ish = 52*5

    closing_price = df[close][::-1].tolist()

    price_uptodate = closing_price[-1]

    L = len(closing_price)

    # 52-weeks Highs and Lows
    #
    if L < One_Year_Ish:
        _52_week_low = min(closing_price)
        _52_week_high = max(closing_price)
    else:
        _52_week_low = min(
            closing_price[-One_Year_Ish::]
        )
        _52_week_high = max(
            closing_price[-One_Year_Ish::]
        )

    averages = [50, 150, 200]
    rolling_averages = {}
    for X in averages:
        avg = []
        for idx, ele in enumerate(closing_price):
            if idx < L - One_Year_Ish:
                continue
            x_ = sum(closing_price[idx - X: idx]) / X
            avg.append(x_)
        rolling_averages[X] = avg[-1]

    score = 0
    # Test 1: Current price above 150- and 200-day averages
    if (price_uptodate > rolling_averages[150]) and (price_uptodate > rolling_averages[200]):
        score += 1

    # Test 2: 150- above 200-day average
    if rolling_averages[150] > rolling_averages[200]:
        score += 1

    # Test 3: 50-day average is above both 150- and 200-day averages
    if (rolling_averages[50] > rolling_averages[200]) and (rolling_averages[50] > rolling_averages[150]):
        score += 1

    # Test 4: Current price is above 50-day average
    if price_uptodate > rolling_averages[50]:
        score += 1

    # Test 5: Current price is at least 30% above 52-week low
    if price_uptodate >= (1.25 * _52_week_low):
        score += 1

    # Test 6: Current price is within 25% of the 52-week high
    if 0.75*_52_week_high <= price_uptodate <= 1.25*_52_week_high:
        score += 1

    return score
