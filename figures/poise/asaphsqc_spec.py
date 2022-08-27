import penguins as pg
import aptenodytes as apt


apt.thesis()

p = apt.nmrd() / "HSQC_OptScan"

f2_bounds=(7.1, 7.78)

dss = [pg.read(p, expno) for expno in (107, 126)]
print([ds['cnst3'] for ds in dss])

# plot 2Ds
fig, axs = pg.subplots2d(1, 2, figsize=(5.2, 2.6), width_ratios=[1, 1.2])
dss[0].stage(ax=axs[0], levels=1e5, f1_bounds="115.1..133", f2_bounds=f2_bounds)
pg.mkplot(axs[0])

# get projections and calculate sensitivity gains
projs = [ds.f2projp() for ds in dss]
peaks = (7.63, 7.54, 7.38, 7.20)
integs = [[proj.integrate(peak, margin=0.02, mode="max") for peak in peaks]
          for proj in projs]
gains = [(integs[1][n]/integs[0][n] - 1) * 100 for n in range(4)]
# plot projections
projs[0].stage(ax=axs[-1], bounds=f2_bounds, color="#404040",
               linestyle="--", linewidth=0.8, zorder=1)
projs[1].stage(ax=axs[-1], bounds=f2_bounds, color=apt.PAL[2],
               linestyle="-", linewidth=0.8)
pg.mkplot(axs[-1])
# enforce xlims to make sure that it lines up with 2D spectra
axs[-1].set_xlim(f2_bounds[1], f2_bounds[0])  # reverse order
for i, (peak, gain) in enumerate(zip(peaks, gains)):
    voffset = 7e4 if i ==0 else 4e4
    axs[-1].text(x=peak, y=projs[1].integrate(peak, margin=0.02, mode="max")+voffset,
                 s=f"+{gain:.0f}%", transform=axs[-1].transData, fontsize=10,
                 horizontalalignment="center")
ymin, ymax = axs[-1].get_ylim()
axs[-1].set_ylim(ymin, ymax*1.1)

pg.ymove(axs[0])


apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
