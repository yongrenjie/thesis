import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / "210126-7a-hsqct-full"
dss = pg.read(p, [36001, 36002, 36003])

fig, axs = pg.subplots2d(1, 3, figsize=(6.5, 2.3))
h1b = (0.4, 7)
c13b = (12, 150)

dss[0].stage(ax=axs[0], levels=4e3, f1_bounds=c13b, f2_bounds=h1b)
dss[1].stage(ax=axs[1], levels=4e3, f1_bounds=c13b, f2_bounds=h1b)
dss[2].stage(ax=axs[2], levels=1e5, f1_bounds=h1b, f2_bounds=h1b)

for ax in axs:
    pg.mkplot(ax)
    pg.ymove(ax)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
