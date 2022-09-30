import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '220604-7x-abbs'
d = pg.read(p, 102)
dss = pg.read(p, range(102001, 102005))

fig, axs = pg.subplots2d(2, 2, figsize=(5, 4.8))

h1_bounds1 = (1, 8.2)
h1_bounds2 = (1, 4.2)
c13_bounds1 = (20, 175)
c13_bounds2 = (20, 135)
n15_bounds = (20, 160)

dss[0].stage(ax=axs[0][0], levels=6e4, f1_bounds=c13_bounds1, f2_bounds=h1_bounds1)
dss[1].stage(ax=axs[0][1], levels=3.6e4, f1_bounds=n15_bounds, f2_bounds=h1_bounds2)
dss[2].stage(ax=axs[1][0], levels=1.7e5, f1_bounds=c13_bounds1, f2_bounds=h1_bounds1)
dss[3].stage(ax=axs[1][1], levels=2.5e5, f1_bounds=c13_bounds2, f2_bounds=h1_bounds1)

pg.mkplots(axs)
pg.ymove(axs)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
