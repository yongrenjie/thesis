import penguins as pg
import aptenodytes as apt
from matplotlib.patches import Rectangle

apt.thesis()
p = apt.nmrd() / '220224-7z-rscbook'

noah_s = pg.read(p, 11001)
noah_c = pg.read(p, 11002)
conv_s = pg.read(p, 23)
conv_c = pg.read(p, 24)
dss = [noah_s, noah_c, conv_s, conv_c]

levels = [1.8e4, 1e6, 1.8e4, 1e6]
h1b_cosy = (1.8, 11)
h1b_hsqc = (1.8, 7.5)
c13b = (20, 126)
f1bs = [c13b, h1b_cosy, c13b, h1b_cosy]
f2bs = [h1b_hsqc, h1b_cosy, h1b_hsqc, h1b_cosy]

# plot spectra
fig, axs = pg.subplots(2, 2, figsize=(6, 5.8))
for ds, ax, f1b, f2b, lev in zip(dss, axs.flat, f1bs, f2bs, levels):
    ds.stage(ax, levels=lev, f1_bounds=f1b, f2_bounds=f2b)
    pg.mkplot(ax)
    pg.ymove(ax)

# show COSY artefacts
x = 2.05
w = 2.45
axs[1][1].add_patch(Rectangle(xy=(x, x+conv_c["sw"][0]/2), width=w, height=w,
                              edgecolor='red', fill=False, linestyle="--",
                              transform=axs[1][1].transData))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
