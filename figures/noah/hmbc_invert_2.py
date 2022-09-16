import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / '211227-7a-hmbc-sehsqc'
dss = pg.read(p, [23003, 24003, 33003, 34003])

fig, axs = pg.subplots2d(2, 2, figsize=(4.5, 4.2))
b = (4.3, 6.8)

for ds, ax in zip(dss, axs.flat):
    ds.stage(ax=ax, levels=5e3, f1_bounds=b, f2_bounds=b)
    pg.mkplot(ax)
    pg.ymove(ax)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
