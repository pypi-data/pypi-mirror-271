import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from mplex.transforms import get_shifted_trans_axes
from mplex.utils import safe_unpack


def add_bar(axs: np.ndarray, fro=0, to=-1, side="t", pad=0, **kwargs):
    side = side.lower()

    lines = {}

    if "t" in side:
        lines["t"] = add_line_across_axes(
            (0, 1), (1, 1), axs[0, fro], axs[0, to], ypad=pad, **kwargs
        )
    if "b" in side:
        lines["b"] = add_line_across_axes(
            (0, 0), (1, 0), axs[-1, fro], axs[-1, to], ypad=-pad, **kwargs
        )
    if "l" in side:
        lines["l"] = add_line_across_axes(
            (0, 1), (0, 0), axs[fro, 0], axs[to, 0], xpad=-pad, **kwargs
        )
    if "r" in side:
        lines["r"] = add_line_across_axes(
            (1, 1), (1, 0), axs[fro, -1], axs[to, -1], xpad=pad, **kwargs
        )
    return lines


def add_line_across_axes(
    p1,
    p2,
    ax1: Axes,
    ax2: Axes,
    trans1="axes",
    trans2="axes",
    xpad=0,
    ypad=0,
    unit="pt",
    **kwargs,
):
    from matplotlib.patches import ConnectionPatch

    xpad, ypad = safe_unpack(xpad), safe_unpack(ypad)
    pad1, pad2 = zip(xpad, ypad)
    trans1 = get_shifted_trans_axes(*pad1, ax1, unit, transform=trans1)
    trans2 = get_shifted_trans_axes(*pad2, ax2, unit, transform=trans2)
    return ax1.add_artist(ConnectionPatch(p1, p2, trans1, trans2, **kwargs))


def add_scale_bars(
    x0,
    y0,
    dx=None,
    dy=None,
    xlabel=None,
    ylabel=None,
    pad=2,
    lw=0.5,
    c="k",
    ls="-",
    size=6,
    fmt="{} ",
    text_kw=None,
    line_kw=None,
    transform="data",
    ax=None,
):
    if ax is None:
        ax = plt.gca()

    line_kw_default = dict(clip_on=False)
    if line_kw is not None:
        line_kw_default.update(**line_kw)
    line_kw = line_kw_default

    lwx, lwy = safe_unpack(lw)
    cx, cy = safe_unpack(c)
    lsx, lsy = safe_unpack(ls)
    size_x, size_y = safe_unpack(size)
    xpad, ypad = safe_unpack(pad)
    kw = dict(
        textcoords="offset points",
        rotation_mode="anchor",
        ha="center",
        annotation_clip=False,
    )

    if transform == "axes":
        kw["xycoords"] = ax.transAxes
        line_kw["transform"] = ax.transAxes

    kwx = dict(rotation=0, va="top", size=size_x, **kw)
    kwy = dict(rotation=90, va="baseline", size=size_y, **kw)
    kwx_, kwy_ = safe_unpack(text_kw)
    if kwx_ is not None:
        kwx.update(**kwx_)
    if kwy_ is not None:
        kwy.update(**kwy_)

    kwx["size"] = size_x
    kwy["size"] = size_y

    ret = dict()

    if dx:
        ret["line_x"] = ax.plot(
            [x0, x0 + dx], [y0, y0], lw=lwx, c=cx, ls=lsx, **line_kw
        )
        xlabel = fmt.format(dx) + str(xlabel)
        ret["text_x"] = ax.annotate(
            xlabel,
            (x0 + dx / 2, y0),
            xytext=(0, -xpad),
            **kwx,
        )

    if dy:
        ret["line_y"] = ax.plot(
            [x0, x0], [y0, y0 + dy], lw=lwy, c=cy, ls=lsy, **line_kw
        )
        ylabel = fmt.format(dy) + str(ylabel)
        ret["text_y"] = ax.annotate(
            ylabel,
            (x0, y0 + dy / 2),
            xytext=(-ypad, 0),
            **kwy,
        )

    return ret
