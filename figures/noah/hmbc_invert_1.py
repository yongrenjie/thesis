import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / '220214-7z-bsx-invert'
dss = pg.read(p, [11003, 13003, 12004])

fig, axs = pg.subplots2d(1, 3, figsize=(6.5, 2.3))
b = (2.05, 4.5)

for ds, ax in zip(dss, axs):
    ds.stage(ax=ax, levels=1e5, f1_bounds=b, f2_bounds=b)
    pg.mkplot(ax)
    pg.ymove(ax)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
