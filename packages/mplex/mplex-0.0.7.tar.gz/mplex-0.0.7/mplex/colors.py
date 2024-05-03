import numpy as np
from matplotlib import colors


def change_alpha(c, a):
    return colors.to_rgb(c) + (a,)


def change_hsv(c, h=None, s=None, v=None):
    hsv = list(colors.rgb_to_hsv(colors.to_rgb(c)))
    if h is not None:
        hsv[0] = h
    if s is not None:
        hsv[1] = s
    if v is not None:
        hsv[2] = v

    return colors.hsv_to_rgb(hsv)


def remove_bg(c, bg):
    if colors.to_hex(bg) == "#ffffff":
        c = np.array(colors.to_rgb(c))
        a = max(1 - c)

        if a == 0:
            return 0, 0, 0, 0

        r, g, b = (c - 1) / a + 1

        return r, g, b, a
    elif colors.to_hex(bg) == "#000000":
        c = 1 - np.array(colors.to_rgb(c))
        r, g, b, a = remove_bg(c, "w")
        return 1 - r, 1 - g, 1 - b, a
    else:
        raise NotImplementedError


def to_gray(c):
    r, g, b = colors.to_rgb(c)
    return r * 0.2126 + g * 0.7152 + b * 0.0722
