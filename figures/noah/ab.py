import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / '211231-7t-adeq'
dss = pg.read(p, [11001, 11002])

fig, axs = pg.subplots2d(1, 2, figsize=(5, 2.4))
levels = [1.2e3, 1.2e5]

for ds, ax, l in zip(dss, axs.flat, levels):
    ds.stage(ax, levels=l, f1_bounds="102..171", f2_bounds="6.3..7.7")
    pg.mkplot(ax)
    pg.ymove(ax)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
