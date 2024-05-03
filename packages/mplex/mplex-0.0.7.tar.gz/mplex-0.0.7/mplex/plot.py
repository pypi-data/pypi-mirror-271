import numpy as np


def cplot(x, y, c=None, cmap="viridis", vmin=0, vmax=1, *, ax, **kwargs):
    from matplotlib import colormaps
    from matplotlib.collections import LineCollection
    from matplotlib.colors import Normalize, is_color_like

    assert len(x) == len(y)
    n = len(x)

    if c is None:
        c = np.linspace(0, 1, n - 1)

    c = np.array(list(c))

    if not is_color_like(c[0]):
        cmap = colormaps.get_cmap(cmap)
        norm = Normalize(vmin, vmax, clip=True)
        colors = cmap(norm(c))
    else:
        colors = c

    points = np.column_stack([x, y])[:, None]
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = LineCollection(segments, colors=colors, **kwargs, capstyle="round")
    ax.autoscale()

    return ax.add_collection(lc)
