def focallength(vanx, vany, xx, xy):
    radius = (((vanx - xx) ** 2 + (vany - xy) ** 2) ** (0.5)) / 2.0
    midy = (vany + xy) / 2.0
    return (radius ** 2 - midy ** 2) ** (0.5)
