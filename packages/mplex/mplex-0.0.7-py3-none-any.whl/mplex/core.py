from typing import Sequence, Union

SIDE_NAMES = ("left", "right", "bottom", "top")
LOC_NAMES = ("lb", "lc", "lt", "cb", "cc", "ct", "rb", "rc", "rt")
LOC_NAME_TO_XY = dict(
    zip(LOC_NAMES, ((i / 2, j / 2) for i in range(3) for j in range(3)))
)


def get_ha(s: str):
    s = s.strip().lower()
    return dict(c="center", l="left", r="right").get(s, s)


def get_va(s: str):
    s = s.strip().lower()
    return dict(c="center", b="bottom", t="top", _="baseline").get(s, s)


def get_orientation(s: str):
    s = s.strip().lower()
    return dict(h="horizontal", v="vertical").get(s, s)


def get_share_ax_name(s: Union[None, bool, str]):
    try:
        if isinstance(s, str):
            s = s.strip().lower()[0]
            return {"a": "all", "r": "row", "c": "col", "n": "none"}[s]

        return {None: "none", False: "none", True: "all"}[s]
    except KeyError:
        raise ValueError(f"Invalid share ax: {s}")


def get_side_names(s: Union[bool, str, Sequence[str]]):
    if isinstance(s, bool):
        return SIDE_NAMES if s else ()

    if not isinstance(s, str):
        s = "".join(s)

    s = s.lower()

    if "a" in s:
        return SIDE_NAMES

    for name in SIDE_NAMES:
        s = s.replace(name, name[0])

    return tuple(name for name in SIDE_NAMES if name[0] in s)


def get_loc_name(loc: str):
    loc = loc.strip().lower()
    for s in ("left", "right", "bottom", "top"):
        loc = loc.replace(s, s[0])

    loc = loc.replace("upper", "t")
    loc = loc.replace("lower", "b")

    if loc in ("l", "r", "c"):
        loc = loc + "c"
    elif loc in ("b", "t"):
        loc = "c" + loc

    if loc in LOC_NAMES:
        return loc
    elif loc[::-1] in LOC_NAMES:
        return loc[::-1]

    raise ValueError(f"Invalid loc string: {loc}")
