import matplotlib.pyplot as plt

from mplex import core


def add_text(
    x,
    y,
    s,
    pad=0,
    transform="data",
    pad_unit="offset points",
    ha="l",
    va="b",
    outline_kwargs=None,
    ax=None,
    **kwargs,
):
    import matplotlib.pyplot as plt

    from mplex.utils import safe_unpack

    pad = safe_unpack(pad)

    if ax is None:
        ax = plt.gca()

    if isinstance(transform, str):
        transform = transform.strip().lower()[0]
        transform = dict(
            d=ax.transData,
            x=ax.get_xaxis_transform(),
            y=ax.get_yaxis_transform(),
        ).get(transform, ax.transAxes)

    if len(ha) == 1:
        ha = core.get_ha(ha)

    if len(va) == 1:
        va = core.get_va(va)

    text = ax.annotate(s, (x, y), pad, transform, pad_unit, ha=ha, va=va, **kwargs)

    if outline_kwargs is not None:
        set_text_outline(text, **outline_kwargs)

    return text


def set_text_outline(text, lw=2, c="w", **kwargs):
    from matplotlib import patheffects

    kwargs = dict(dict(linewidth=lw, foreground=c), **kwargs)
    text.set_path_effects([patheffects.Stroke(**kwargs), patheffects.Normal()])


def get_text_bbox(text, ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    remove = False
    kwargs = dict(dict(x=0, y=0), **kwargs)
    r = ax.figure.canvas.get_renderer()
    if isinstance(text, str):
        text = ax.text(text, **kwargs)
        remove = True
    bb = text.get_window_extent(renderer=r)
    if remove:
        text.remove()
    return bb


def get_text_size(text, ax=None, **kwargs):
    bb = get_text_bbox(text, ax=ax, **kwargs)
    return bb.width, bb.height
