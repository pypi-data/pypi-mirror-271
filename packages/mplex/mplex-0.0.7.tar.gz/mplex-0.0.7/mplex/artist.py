from matplotlib.artist import Artist


def add_outline(artist: Artist, c="w", lw=1, back=True, **kwargs):
    from matplotlib.patheffects import Normal, Stroke

    effects = artist.get_path_effects()

    if not effects:
        effects = [Normal()]

    stroke = Stroke(linewidth=lw, foreground=c, **kwargs)
    effects.insert(0 if back else len(effects), stroke)
    artist.set_path_effects(effects)
