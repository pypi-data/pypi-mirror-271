import matplotlib as mpl

# import matplotlib.pylab as plt
from cycler import cycler

from .constants import colors


def mm_to_inch(mm: float) -> float:
    return mm / 25.4


def make_default_colors():
    mpl.rcParams.update(
        {
            "axes.prop_cycle": cycler("color", colors),
        }
    )


def make_default_font_size():
    mpl.rcParams.update(
        {
            "font.size": 12,
            "axes.titlesize": 12,
            "axes.labelsize": 12,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 12,
            "figure.titlesize": 12,
        }
    )


# def reset
