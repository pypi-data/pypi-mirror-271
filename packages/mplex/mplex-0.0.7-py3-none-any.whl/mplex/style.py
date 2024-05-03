from pathlib import Path

import matplotlib.pyplot as plt


def get_style(style="default"):
    """Get custom Matplotlib style.

    Parameters
    ----------
    style

    Returns
    -------

    """
    path = Path(__file__).parent / "stylesheets" / f"{style}.mplstyle"
    if path.exists():
        return path
    return style


def use_style(style="default"):
    import matplotlib._mathtext as mathtext

    mathtext.FontConstantsBase.sup1 = 0.35

    plt.style.use(get_style(style))
