import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '210722-7c-tsnoah'
dss = pg.read(p, range(109001, 109009))

fig, axs = pg.subplots(3, 3, figsize=(6.5, 6))
axs[2][2].remove(); axs = axs.flat[:8]

dss[0].stage(ax=axs[0], levels=4e2, f1_bounds="", f2_bounds="0.3..8.5")
dss[1].stage(ax=axs[1], levels=4e2, f1_bounds="", f2_bounds="0.3..8.5")
dss[2].stage(ax=axs[2], levels=2e3, f1_bounds="..136", f2_bounds="0.3..8.5")
dss[3].stage(ax=axs[3], levels=2e3, f1_bounds="..136", f2_bounds="0.3..8.5")
dss[4].stage(ax=axs[4], levels=1e3, f1_bounds="..136", f2_bounds="0.3..8.5")
dss[5].stage(ax=axs[5], levels=1e3, f1_bounds="..136", f2_bounds="0.3..8.5")
dss[6].stage(ax=axs[6], levels=3e4, f1_bounds="0.3..8.5", f2_bounds="0.3..8.5")
dss[7].stage(ax=axs[7], levels=3e4, f1_bounds="0.3..8.5", f2_bounds="0.3..8.5")

for ax in axs:
    pg.mkplot(ax)
    pg.ymove(ax)

for ax in axs[-2:]:
    pos = ax.get_position()
    pos.x0 = pos.x0 + 1/6
    pos.x1 = pos.x1 + 1/6
    ax.set_position(pos)

apt.label_axes_def(axs, start=2)
# apt.show()
apt.save(__file__, svg=True)
