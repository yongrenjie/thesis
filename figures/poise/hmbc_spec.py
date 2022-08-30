import penguins as pg
import aptenodytes as apt

apt.thesis()

path = apt.nmrd() / '210814-7z-lpjf-opt'
unopt = pg.read(path, 11)
opt = pg.read(path, 12)
lp3 = pg.read(path, 13)

f1b = "111..130"
f2b = "6.5..7.8"
levels = 7e4

fig, axs = pg.subplots(1, 3, figsize=(6.5, 2.2))

for ax, ds in zip(axs, [unopt, opt, lp3]):
    ds.stage(ax=ax, levels=levels, f1_bounds=f1b, f2_bounds=f2b)
    pg.mkplot(ax)
    pg.ymove(ax)

from matplotlib.patches import Rectangle
axs[0].add_patch(Rectangle(xy=(7.15, 118.0), width=0.45, height=2.4,
                           edgecolor='red', fill=False))
axs[0].add_patch(Rectangle(xy=(6.72, 121.7), width=0.45, height=2.4,
                           edgecolor='red', fill=False))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
