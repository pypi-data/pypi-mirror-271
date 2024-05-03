from itertools import product, zip_longest

import numpy as np
from matplotlib.gridspec import GridSpec

from mplex import core
from mplex.axes import Axes
from mplex.axes_collection import AxArray2D
from mplex.figure import Figure
from mplex.utils import safe_len, safe_unpack, to_array


def _get_shared_ax(row: int, col: int, how: str, axs: np.ndarray):
    how = core.get_share_ax_name(how)
    return {"row": axs[row, 0], "col": axs[0, col], "all": axs[0, 0]}.get(how, None)


class Grid(Figure):
    def __init__(
        self,
        axsize=(100, 100),
        shape=(None, None),
        space=(0, 0),
        border=(0, 0, 0, 0),
        figsize=(None, None),
        unit="pt",
        spines="a",
        sharex="a",
        sharey="a",
        tickdir="oo",
        ticks_sides="lb",
        ticklabels_sides="lb",
        keep_inner_ticklabels=None,
        **kwargs,
    ):
        axw, axh = safe_unpack(axsize)
        nrow, ncol = safe_unpack(shape, default1=1)
        figw, figh = safe_unpack(figsize)

        nrow = safe_len(axh) if nrow is None else nrow
        ncol = safe_len(axw) if ncol is None else ncol

        axw = to_array(axw, ncol)
        axh = to_array(axh, nrow)

        assert len(axw) == ncol
        assert len(axh) == nrow

        wspace, hspace = safe_unpack(space)
        wspace = to_array(wspace, ncol - 1)
        hspace = to_array(hspace, nrow - 1)

        if len(wspace) < ncol - 1:
            wspace = wspace[np.arange(ncol - 1) % len(wspace)]

        if len(hspace) < nrow - 1:
            hspace = hspace[np.arange(nrow - 1) % len(hspace)]
        
        if not hasattr(border, "__len__"):
            border = (border, border, border, border)
        elif len(border) == 2:
            border = (border[0], border[0], border[1], border[1])

        if len(wspace) == ncol - 1:
            wspace = np.array((border[0], *wspace, border[1]))

        if len(hspace) == nrow - 1:
            hspace = np.array((border[2], *hspace, border[3]))

        assert len(wspace) == ncol + 1
        assert len(hspace) == nrow + 1

        gridw = np.array(sum(zip_longest(wspace, axw), ())[:-1])
        gridh = np.array(sum(zip_longest(hspace, axh), ())[:-1])

        if figw not in (None, "auto"):
            scale = figw / gridw.sum()
            gridw = gridw * scale

            if figh == "auto":
                gridh = gridh * scale

        if figh not in (None, "auto"):
            scale = figh / gridh.sum()
            gridh = gridh * scale
            if figw == "auto":
                gridw = gridw * scale

        super().__init__((gridw.sum(), gridh.sum()), unit, **kwargs)

        self.gridw = gridw
        self.gridh = gridh

        self._gs = GridSpec(
            nrow * 2 + 1, ncol * 2 + 1, width_ratios=gridw, height_ratios=gridh
        )
        self._axes = np.full((nrow, ncol), None, dtype=object)  # noqa
        self._sharex = core.get_share_ax_name(sharex)
        self._sharey = core.get_share_ax_name(sharey)

        for i, j in product(range(nrow), range(ncol)):
            self._axes[i, j] = Axes(
                self._fig,
                self._gs[i * 2 + 1, j * 2 + 1],
                sharex=_get_shared_ax(i, j, self._sharex, self._axes),
                sharey=_get_shared_ax(i, j, self._sharey, self._axes),
            )
            self._fig.add_subplot(self._axes[i, j])

        self._ca = self[:]

        ticks_sides = core.get_side_names(ticks_sides)
        self._ticklabels_sides = (
            ticks_sides
            if ticklabels_sides is None
            else core.get_side_names(ticklabels_sides)
        )
        self._ca.set_visible(
            ticks=ticks_sides, ticklabels=self._ticklabels_sides, spines=spines
        )
        self._ca.set_tick_direction(tickdir)

        if keep_inner_ticklabels is None:
            self._ca.remove_inner_ticklabels(sharex, sharey, ticklabels_sides)
        elif keep_inner_ticklabels is False:
            self._ca.remove_inner_ticklabels()

    def __getattr__(self, name):
        return getattr(self._ca, name)

    def __getitem__(self, key):
        axs = np.matrix(self.axs)[key]
        if isinstance(axs, np.matrix):
            return AxArray2D(np.array(axs))
        return axs

    @property
    def nrows(self):
        return self._axes.shape[0]

    @property
    def ncols(self):
        return self._axes.shape[1]

    @property
    def axs(self):
        return self._axes

    @property
    def ca(self):
        """Current axes"""
        return self._ca

    @property
    def fig(self):
        return self._fig

    @property
    def gs(self):
        return self._gs

    def sca(self, *keys):
        """Set current axes"""
        self._ca = self[keys]

    def to_rgba_array(self):
        canvas = self.fig.canvas
        canvas.draw()
        img = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
        img = img.reshape(canvas.get_width_height()[::-1] + (4,))
        return img
