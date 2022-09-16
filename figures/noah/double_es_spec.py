import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / '211105-4s-cx-solvsupp'
dss = pg.read(p, [21002, 21003, 11002, 11003])

fig, axs = pg.subplots2d(2, 2, figsize=(4.7, 4.5))
cosy_l = 1e9
tocsy_l = 1e8
levels = (cosy_l, tocsy_l, cosy_l, tocsy_l)
b = (3.1, 5.6)

for ds, ax, l in zip(dss, axs.flat, levels):
    ds.stage(ax=ax, levels=l, f1_bounds=b, f2_bounds=b)
    pg.mkplot(ax)
    pg.ymove(ax)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
