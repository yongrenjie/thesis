import penguins as pg
import aptenodytes as apt
from matplotlib.patches import Rectangle

apt.thesis()
p = apt.nmrd() / '210916-7a-hmbc-morescans'
dss = pg.read(p, [4001, 3001, 7, 8])

fig, axs = pg.subplots2d(2, 2, figsize=(4.5, 4.2))

for ds, ax in zip(dss, axs.flat):
    ds.stage(ax, levels=5e3, f1_bounds="32..84", f2_bounds="3..5.2")
    pg.mkplot(ax)
    pg.ymove(ax)

axs[0][0].add_patch(Rectangle((3.84, 73.3), 0.77, 2.8, fill=False, color='red'))
axs[0][0].add_patch(Rectangle((3.70, 61.5), 0.3, 2.8, fill=False, color='red'))
axs[0][0].add_patch(Rectangle((4.72, 63.2), 0.4, 2.8, fill=False, color='red'))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
