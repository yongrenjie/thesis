import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '220722-7c-abbs'
dss = pg.read(p, range(14001, 14006))

fig, axs = pg.subplots(2, 3, figsize=(6.5, 4.2))
axs[1][2].remove(); axs = axs.flat[:5]

h1_bounds1 = (0.5, 6.1)
h1_bounds2 = (0.5, 8.5)
h1_bounds3 = (7.2, 8.5)
c13_bounds1 = (6, 178)
c13_bounds2 = (6, 135)
n15_bounds1 = (110, 130)
n15_bounds2 = (114, 130)

dss[0].stage(ax=axs[0], levels=4.5e4, f1_bounds=c13_bounds1, f2_bounds=h1_bounds1)
dss[1].stage(ax=axs[1], levels=1.8e4, f1_bounds=n15_bounds1, f2_bounds=h1_bounds1)
dss[2].stage(ax=axs[2], levels=2.5e5, f1_bounds=c13_bounds1, f2_bounds=h1_bounds2)
dss[3].stage(ax=axs[3], levels=2.5e5, f1_bounds=n15_bounds2, f2_bounds=h1_bounds3)
dss[4].stage(ax=axs[4], levels=2.5e5, f1_bounds=c13_bounds2, f2_bounds=h1_bounds1)

pg.mkplots(axs)
pg.ymove(axs)
for ax in axs[-2:]:
    pos = ax.get_position()
    pos.x0 = pos.x0 + 1/6
    pos.x1 = pos.x1 + 1/6
    ax.set_position(pos)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
