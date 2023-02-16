import penguins as pg
import aptenodytes as apt
apt.thesis()

p = apt.nmrd() / '220809-6a-hsqc-comparisons'

st_ns2 = pg.read(p, 4)
ea_ns1 = pg.read(p, 4)
st_ns1 = pg.read(p, 6)

fig, axs = apt.subplots2d(2, 2, figsize=(6.5, 6))

st_ns1.stage(axs[0][0], levels=3e3)
ea_ns1.stage(axs[0][1], levels=3e3)
st_ns2.stage(axs[1][0], levels=3e3)

f1_bounds = "60..110"
f2_bounds_signal = "2.9..5.2"
f2_bounds_noise = "6.8..7.9"
st_proj = st_ns1.f2projp(bounds=f1_bounds)
ea_proj = ea_ns1.f2projp(bounds=f1_bounds)
st_proj.stage(axs[1][1], bounds=f2_bounds_signal, label="States–TPPI")
ea_proj.stage(axs[1][1], bounds=f2_bounds_signal, label="echo–antiecho")
ax_inset = pg.mkinset(axs[1][1], size=(0.6, 0.2), pos=(0.35, 0.54),
                      show_zoom=False)
st_proj.stage(ax_inset, bounds=f2_bounds_noise, color=apt.PAL[0])
ea_proj.stage(ax_inset, bounds=f2_bounds_noise, color=apt.PAL[1])

pg.mkplot(axs[0][0])
pg.mkplot(axs[0][1])
pg.mkplot(axs[1][0])
pg.mkplot(axs[1][1], hoffset=0.04)
pg.mkplot(ax_inset, xlabel='')
pg.ymove(axs)
ymin, ymax = axs[1][1].get_ylim()
axs[1][1].set_ylim((ymin, ymax*1.4))
apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
