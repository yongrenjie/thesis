import penguins as pg
import aptenodytes as apt
from matplotlib.patches import Rectangle

apt.thesis()
p = apt.nmrd() / '220224-7z-rscbook'

dss = pg.read(p, range(15001, 15005))

levels = [3.8e3, 1.8e4, 5e5, 5e4]
h1b_cosy = (1.8, 11)
h1b_hsqc = (1.8, 7.5)
c13b = (20, 126)
f1bs = [(20, 163), (20, 126), h1b_cosy, h1b_cosy]
f2bs = [h1b_cosy, h1b_hsqc, h1b_cosy, h1b_cosy]

# plot spectra
fig, axs = pg.subplots(2, 2, figsize=(6, 5.8))
for ds, ax, f1b, f2b, lev in zip(dss, axs.flat, f1bs, f2bs, levels):
    ds.stage(ax, levels=lev, f1_bounds=f1b, f2_bounds=f2b)
    pg.mkplot(ax)
    pg.ymove(ax)

axs[1][0].arrow(x=4.90, y=2.77, dx=-0.3, dy=0, color='black', head_width=0.15)
axs[1][0].arrow(y=4.90, x=2.77, dy=-0.3, dx=0, color='black', head_width=0.15)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
