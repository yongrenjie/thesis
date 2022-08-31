import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / "Solvsupp_Opt"

dss = [pg.read(p, expno) for expno in [2, 31, 35, 36, 37]]

fig, ax = pg.subplots(figsize=(6.5, 5))
for ds, color in zip(dss, ['black', *apt.PAL]):
    ds.stage(bounds="3.5..5.4", color=color)
pg.mkplot(voffset=1.1)

# Easier to manually do this...
titles = (
    "initial point for optimisation",
    "1 parameter optimised (4 min 21 sec)",
    "2 parameters optimised (12 min 19 sec)",
    "3 parameters optimised (17 min 23 sec)",
    "4 parameters optimised (26 min 20 sec)",
)

for i, (voffset, color, ds, title) in enumerate(zip(ax.prop.voffsets,
                                                    ax.prop.colors,
                                                    dss,
                                                    titles)):
    height = voffset + 5e8
    ax.text(x=0.95, y=height, s=title,
            color=color, transform=ax.get_yaxis_transform(),
            horizontalalignment="right")
pg.style_axes(ax, "1d")

# apt.show()
apt.save(__file__)
