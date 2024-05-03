import matplotlib.pyplot as plt

from mplex.utils import convert_unit


def get_shifted_trans_axes(
    dx=0,
    dy=0,
    ax: plt.Axes = None,
    unit="pt",
    transform="axes",
):
    from matplotlib.transforms import ScaledTranslation

    if ax is None:
        ax = plt.gca()

    dx, dy = convert_unit((dx, dy), fro=unit, to="inch")

    translate = ScaledTranslation(dx, dy, ax.get_figure().dpi_scale_trans)

    if transform == "x":
        return ax.get_xaxis_transform() + translate

    if transform == "y":
        return ax.get_yaxis_transform() + translate

    if transform == "axes":
        return ax.transAxes + translate

    if transform == "data":
        return ax.transData + translate

    return translate
