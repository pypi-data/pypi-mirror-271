from typing import Callable

import numpy as np
from matplotlib import cm, colors

from mplex.colors import remove_bg


def map_cmap(func: Callable, cmap: str | colors.Colormap, lut=None):
    from matplotlib.colors import ListedColormap

    if isinstance(cmap, list):
        cmap = ListedColormap(cmap)
    cmap = cm.get_cmap(cmap, lut)
    return colors.ListedColormap([func(cmap(i)) for i in np.linspace(0, 1, cmap.N)])


def get_transparent_cmap(cmap, bg, lut=None):
    return map_cmap(lambda c: remove_bg(c, bg), cmap, lut)


def lerp_colors(c1, c2, n=256, as_cmap=True, color_space="lab"):
    from colormath.color_conversions import convert_color
    from colormath.color_objects import LabColor, LuvColor, sRGBColor
    from matplotlib.colors import to_rgb

    color_space = dict(lab=LabColor, luv=LuvColor)[color_space]

    c1 = convert_color(sRGBColor(*to_rgb(c1)), color_space)
    c2 = convert_color(sRGBColor(*to_rgb(c2)), color_space)

    colors = np.linspace(c1.get_value_tuple(), c2.get_value_tuple(), n)
    colors = np.array(
        [convert_color(color_space(*i), sRGBColor).get_value_tuple() for i in colors]
    )
    colors = np.clip(colors, 0, 1)

    if as_cmap:
        from matplotlib.colors import ListedColormap

        return ListedColormap(colors)

    return colors
