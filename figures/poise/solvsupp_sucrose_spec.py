import penguins as pg
import aptenodytes as apt

apt.thesis()
path = apt.nmrd() / "210617-4s-solvsupp-opt"

dss = [pg.read(path, expno) for expno in range(10, 15)]
titles = ["initial point for optimisation",
          "1 parameter optimised (10 min 50 sec)",
          "2 parameters optimised (13 min 45 sec)",
          "3 parameters optimised (14 min 23 sec)",
          "4 parameters optimised (23 min 16 sec)"]

fig, ax = pg.subplots(figsize=(6.5, 5))
for ds, color in zip(dss, ['black', *apt.PAL]):
    ds.stage(bounds="3.3..5.4", color=color)
pg.mkplot(voffset=1.1)

for i, (voffset, color, ds, title) in enumerate(zip(ax.prop.voffsets,
                                                    ax.prop.colors,
                                                    dss,
                                                    titles)):
    height = voffset + 1e11
    ax.text(x=0.95, y=height, s=title,
            color=color, transform=ax.get_yaxis_transform(),
            horizontalalignment="right")
pg.style_axes(ax, "1d")

# apt.show()
apt.save(__file__)
