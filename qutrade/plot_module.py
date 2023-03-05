##### MARKED FOR DELETION

import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import numpy as np


def plot_graph(name, dates, closing_price, volume, rolling_averages, years: int = 1):
    averages = [50, 150, 200]
    L = len(closing_price)

    if np.floor(L / (52 * 5)) > 1:
        outname = name + f"_{years}years.pdf"
    else:
        outname = name + ".pdf"

    mpl.style.use("seaborn")
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["font.family"] = "STIXGeneral"
    mpl.rcParams["axes.linewidth"] = 1.2

    nticks = 30
    tick_dates = dates[0 : L - 1 : nticks]

    labels = []
    for str in tick_dates:
        frmt = datetime.strptime(str, "%Y-%m-%d")
        newfrmt = frmt.strftime("%d %b %y")
        labels.append(newfrmt)

    w = 15
    h = 7
    d = 70

    plt.figure(figsize=(w, h), dpi=d)

    f1 = plt.subplot(2, 1, 1)
    plt.plot(dates, closing_price, color="grey")
    for idx, X in enumerate(averages):
        plt.plot(dates, rolling_averages[idx], label="%s-day avg" % X)
    # input_csv['Date'][ticks], labels, rotation = 30, fontsize = 15)
    plt.setp(f1.get_xticklabels(), visible=False)

    plt.legend(fontsize=18)
    plt.ylabel("Price", fontsize=18)
    plt.grid(True)

    f2 = plt.subplot(2, 1, 2, sharex=f1)
    plt.plot(dates, volume)
    plt.xticks(tick_dates, labels, rotation=30, fontsize=15)
    plt.tick_params(direction="out", length=6, width=2, grid_alpha=0.5)
    plt.ylabel("Volume", fontsize=18)
    plt.tight_layout()
    plt.savefig(outname, bbox_inches="tight")
