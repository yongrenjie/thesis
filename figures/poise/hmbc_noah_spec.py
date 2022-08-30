import penguins as pg
import aptenodytes as apt

apt.thesis()

path = apt.nmrd() / '210814-7z-zzlpjf-opt'
unopt = pg.read(path, 11001)
opt = pg.read(path, 12001)
lp3 = pg.read(path, 13001)

f1b = "36..71"
f2b = "2.0..4.5"
levels = 5e3

fig, axs = pg.subplots(1, 3, figsize=(6.5, 2.2))

for ax, ds in zip(axs, [unopt, opt, lp3]):
    ds.stage(ax=ax, levels=levels, f1_bounds=f1b, f2_bounds=f2b)
    pg.mkplot(ax)
    pg.ymove(ax)

from matplotlib.patches import Rectangle
axs[0].add_patch(Rectangle(xy=(2.40, 58.4), width=0.35, height=3.0,
                           edgecolor='red', fill=False, zorder=1))
axs[0].add_patch(Rectangle(xy=(4.03, 66.9), width=0.39, height=3.0,
                           edgecolor='red', fill=False, zorder=1))
axs[0].add_patch(Rectangle(xy=(2.34, 43.9), width=0.14, height=2.7,
                           edgecolor='red', fill=False, zorder=1))
axs[0].add_patch(Rectangle(xy=(2.07, 43.9), width=0.14, height=2.7,
                           edgecolor='red', fill=False, zorder=1))
axs[0].add_patch(Rectangle(xy=(2.55, 38.8), width=0.14, height=2.4,
                           edgecolor='red', fill=False, zorder=1))
axs[0].add_patch(Rectangle(xy=(2.31, 38.8), width=0.14, height=2.4,
                           edgecolor='red', fill=False, zorder=1))
axs[0].add_patch(Rectangle(xy=(4.09, 52.5), width=0.23, height=2.1,
                           edgecolor='red', fill=False, zorder=1))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
