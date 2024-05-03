from typing import Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

from mplex import core, utils
from mplex.utils import convert_unit


class Axes(plt.Axes):
    def add_text(
        self,
        x,
        y,
        s,
        pad=0,
        transform="data",
        pad_unit="offset points",
        ha="l",
        va="b",
        **kwargs,
    ):
        from mplex.text import add_text

        return add_text(
            x,
            y,
            s,
            pad=pad,
            transform=transform,
            pad_unit=pad_unit,
            ha=ha,
            va=va,
            ax=self,
            **kwargs,
        )

    def add_scale_bars(
        self,
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
    ):
        from mplex.annotate import add_scale_bars

        return add_scale_bars(
            x0,
            y0,
            dx,
            dy,
            xlabel,
            ylabel,
            pad,
            lw,
            c,
            ls,
            size,
            fmt,
            text_kw,
            line_kw,
            transform,
            ax=self,
        )

    def add_colorbar(
        self,
        vmin=0,
        vmax=1,
        cmap="viridis",
        mappable=None,
        length=20,
        thick=5,
        pad=5,
        pad_unit="pt",
        orientation=None,
        loc0="rb",
        loc1=None,
        clip=False,
        length_unit="pt",
        thick_unit="pt",
        ax_kwargs=None,
        **kwargs,
    ):
        from mplex.axes_collection import AxArray

        return AxArray(self).add_colorbar(
            vmin,
            vmax,
            cmap,
            mappable,
            length,
            thick,
            pad,
            pad_unit,
            orientation,
            loc0,
            loc1,
            clip,
            length_unit,
            thick_unit,
            ax_kwargs,
            **kwargs,
        )

    def set_tick_direction(self, directions: str):
        return set_tick_direction(directions, ax=self)

    def set_tight_bounds(self, x=True, y=True):
        return set_tight_bounds(x, y, ax=self)

    def remove_ticklabels_trailing_zeros(self, which="both"):
        return remove_ticklabels_trailing_zeros(which, ax=self)

    def set_visible_sides(
        self, sides=None, *, spines=None, ticks=None, ticklabels=None
    ):
        return set_visible_sides(
            sides, spines=spines, ticks=ticks, ticklabels=ticklabels, ax=self
        )


def set_tick_direction(directions: str, ax: plt.Axes):
    direction_dict = {"i": "in", "o": "out", "b": "inout"}

    if len(directions) == 1:
        directions = directions * 2

    for i, direction in zip("xy", directions):
        if direction.lower() == "n":
            ax.tick_params(i, length=0)
        elif direction in direction_dict:
            direction = direction_dict[direction]
            ax.tick_params(i, direction=direction)


def set_tight_bounds(x=True, y=True, *, ax: plt.Axes):
    a, b = ax.get_xlim()

    if x:
        ticks = ax.get_xticks()
        a = ticks[ticks >= a].min()
        b = ticks[ticks <= b].max()

    ax.spines.bottom.set_bounds(a, b)

    a, b = ax.get_ylim()

    if y:
        ticks = ax.get_yticks()
        a = ticks[ticks >= a].min()
        b = ticks[ticks <= b].max()

    ax.spines.left.set_bounds(a, b)


def remove_ticklabels_trailing_zeros(which="both", *, ax: plt.Axes):
    from matplotlib.ticker import FormatStrFormatter

    if which == "both":
        which = "xy"

    if "x" in which:
        ax.xaxis.set_major_formatter(FormatStrFormatter("%g"))
    if "y" in which:
        ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))


def set_visible_sides(
    sides=None, *, spines=None, ticks=None, ticklabels=None, ax: plt.Axes
):
    if sides is not None:
        spines = ticks = ticklabels = sides

    if ticklabels is None and ticks is not None:
        ticklabels = ticks

    for side in core.SIDE_NAMES:
        if spines is not None:
            ax.spines[side].set_visible(side in core.get_side_names(spines))
        if ticks is not None:
            ax.tick_params(**{side: side in core.get_side_names(ticks)})
        if ticklabels is not None:
            ax.tick_params(**{f"label{side}": side in core.get_side_names(ticklabels)})


def add_axes(
    rect,
    unit: Union[str, Tuple[str, str], Tuple[str, str, str, str]] = "pt",
    loc0="r",
    loc1=None,
    pad: Union[Union[int, float], Tuple[Union[int, float], Union[int, float]]] = 0,
    pad_unit="pt",
    relocate_ticks=False,
    *,
    ax,
    **kwargs,
):
    loc0 = core.get_loc_name(loc0)

    if loc1 is None:
        # get opposite location
        loc1 = tuple(1 - i for i in core.LOC_NAME_TO_XY[loc0])
        loc1 = next(k for k, v in core.LOC_NAME_TO_XY.items() if v == loc1)
    else:
        loc1 = core.get_loc_name(loc1)

    try:
        x, y, w, h = rect
    except TypeError:
        x = y = 0
        w, h = utils.safe_unpack(rect)
    except ValueError:
        x = y = 0
        w, h = utils.safe_unpack(rect)

    if isinstance(unit, str):
        x_unit = y_unit = w_unit = h_unit = unit
    else:
        (x_unit, y_unit), (w_unit, h_unit) = unit[:2], unit[-2:]

    fig = ax.figure
    box = ax.get_position()

    # get size of axes in inches
    ax_size = fig.get_size_inches() * (box.width, box.height)

    if "ax" not in x_unit:
        x = convert_unit(x, x_unit, "inch") / ax_size[0]
    if "ax" not in y_unit:
        y = convert_unit(y, y_unit, "inch") / ax_size[1]

    if w is None:
        w = 1
    elif "ax" not in w_unit:
        w = convert_unit(w, w_unit, "inch") / ax_size[0]

    if h is None:
        h = 1
    elif "ax" not in h_unit:
        h = convert_unit(h, h_unit, "inch") / ax_size[1]

    p0 = core.LOC_NAME_TO_XY[loc0]
    p1 = core.LOC_NAME_TO_XY[loc1]

    x = x + p0[0] - w * p1[0]
    y = y + p0[1] - h * p1[1]

    try:
        dx, dy = pad  # type: ignore
    except TypeError:
        if "c" in loc1 and loc1 != "cc":
            if loc1[0] in ("l", "r"):
                dx, dy = pad, 0
            else:
                dx, dy = 0, pad
        elif loc0 == loc1:
            dx, dy = pad, pad
        elif loc0[1] == loc1[1]:
            dx, dy = pad, 0
        elif loc0[0] == loc1[0]:
            dx, dy = 0, pad
        else:
            dx, dy = pad, pad

    if isinstance(pad_unit, str):
        pad_unit = (pad_unit,) * 2

    dx = convert_unit(dx, pad_unit[0], "inch") / ax_size[0]
    dy = convert_unit(dy, pad_unit[1], "inch") / ax_size[1]

    if loc1[0] == "r":
        dx = -dx

    if loc1[1] == "t":
        dy = -dy

    w, h = box.width * w, box.height * h
    ax2fig = ax.transAxes + fig.transFigure.inverted()
    x, y = ax2fig.transform((x + dx, y + dy))

    new_ax = fig.add_axes((x, y, w, h), **kwargs)

    if relocate_ticks:
        if loc1[0] == "l":
            new_ax.yaxis.tick_right()
        elif loc1[1] == "r":
            new_ax.yaxis.tick_left()

        if loc1[1] == "b":
            new_ax.xaxis.tick_top()
        elif loc1[1] == "t":
            new_ax.xaxis.tick_bottom()

    return new_ax


def add_bounding_axes(*axs: plt.Axes):
    fig: plt.Figure = next(iter(axs)).figure
    assert all(ax.figure is fig for ax in axs)
    trans = fig.transFigure.inverted()
    points = [ax.get_window_extent().transformed(trans).get_points() for ax in axs]
    x, y = np.min(points, (0, 1))
    w, h = np.ptp(points, (0, 1))
    ax = fig.add_axes((x, y, w, h))
    return ax


def get_row_span(*axs: plt.Axes):
    row_spans = [ax.get_subplotspec().rowspan for ax in axs]
    row0 = min(i.start for i in row_spans)
    row1 = max(i.stop for i in row_spans)
    return row0, row1


def get_col_span(*axs: plt.Axes):
    col_spans = [ax.get_subplotspec().colspan for ax in axs]
    col0 = min(i.start for i in col_spans)
    col1 = max(i.stop for i in col_spans)
    return col0, col1


def sharey(*axs):
    for i in range(len(axs) - 1):
        axs[i].sharey(axs[i + 1])


def sharex(*axs):
    for i in range(len(axs) - 1):
        axs[i].share(axs[i + 1])


def sharexy(*axs):
    sharex(*axs)
    sharey(*axs)
