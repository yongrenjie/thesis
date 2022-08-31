import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / "PSYCHE_Opt"

dss = [pg.read(p, expno, 1) for expno in [1, 1400, 1401, 1402, 1403, 1404]]
scales = [0.5, 1, 1, 1, 1, 1]

fig, ax = pg.subplots2d(figsize=(6.5, 5))
for ds, scale, color in zip(dss, scales, ['black', 'black', *apt.PAL]):
    ds.stage(bounds="1.15..2.7", scale=scale, color=color)
pg.mkplot(voffset=1.1)


# Easier to manually do this...
titles = (
    "coupled $^1$H spectrum",
    "initial point for PSYCHE optimisation",
    "1 parameter optimised (2 min 16 sec)",
    "2 parameters optimised (5 min 24 sec)",
    "3 parameters optimised (9 min 53 sec)",
    "4 parameters optimised (13 min 40 sec)",
)

for i, (voffset, color, ds, title) in enumerate(zip(ax.prop.voffsets,
                                                    ax.prop.colors,
                                                    dss,
                                                    titles)):
    height = voffset + 1.2e4
    ax.text(x=1.25,
            y=height,
            s=title,
            color=color,
            transform=ax.transData,
            horizontalalignment="right")
    if i > 0:
        ax.text(x=2.7,
                y=voffset+2e3,
                s="×12",
                color=color,
                transform=ax.transData)
pg.style_axes(ax, "1d")

# apt.show()
apt.save(__file__)
