import penguins as pg
import numpy as np
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / 'NOESY_OptScan'
dss = [pg.read(p, expno, 1) for expno in (104, 135)]

fig, axs = pg.subplots(1, 2, figsize=(5.3, 2.6))
for ds, ax, char in zip(dss, axs, "ab"):
    ds.stage(ax=ax, levels=1e5, f1_bounds="7.1..7.7", f2_bounds="7.1..7.7")
    pg.mkplot(ax)
    pg.ymove(ax)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
