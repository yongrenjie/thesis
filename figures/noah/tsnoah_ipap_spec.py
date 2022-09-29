import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '210722-7c-tsnoah'
dss = pg.read(p, [1009004, 1009003, 1009005, 1009006])

fig, axs = pg.subplots(2, 2, figsize=(5, 4.8))
dss[0].stage(ax=axs[0][0], levels=3e3, f1_bounds="..136", f2_bounds="0.3..8.5")
dss[1].stage(ax=axs[0][1], levels=3e3, f1_bounds="..136", f2_bounds="0.3..8.5")
dss[2].stage(ax=axs[1][0], levels=2e3, f1_bounds="..136", f2_bounds="0.3..8.5")
dss[3].stage(ax=axs[1][1], levels=2e3, f1_bounds="..136", f2_bounds="0.3..8.5")

for ax in axs.flat:
    pg.mkplot(ax)
    pg.ymove(ax)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
