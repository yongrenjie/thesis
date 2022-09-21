import penguins as pg
import aptenodytes as apt
import numpy as np

apt.thesis()
p = apt.nmrd() / '201017-7g-n15-sehsqc-full'
hmqc = pg.read(p, 12001)
hsqc = pg.read(p, 22001)
sehsqc1 = pg.read(p, 32001)
sehsqc2 = pg.read(p, 42001)
dss = [hsqc, sehsqc1, sehsqc2]
titles = ['HSQC', 'seHSQC1', 'seHSQC2']

fig, axs = pg.subplots2d(2, 3, figsize=(6.5, 3.5),
                         height_ratios=[1, 0.6])
f1b, f2b = "111..131", "7..9.3"

# Plot 2D data
for ds, ax, title in zip(dss, axs[0], titles):
    ds.stage(ax=ax, levels=5e3, f1_bounds=f1b, f2_bounds=f2b)
    pg.mkplot(ax)
    ax.text(s=title, x=0.16, y=0.98, ha='left', va='top',
            transform=ax.transAxes)
    pg.ymove(ax)
# Plot projections
for ds, ax in zip(dss, axs[1]):
    ds.f1projp().stage(ax, bounds="111..131")
    pg.mkplot(ax)
# Standardise ylims of projections.
ymin = min(ax.get_ylim()[0] for ax in axs[1])
ymax = max(ax.get_ylim()[1] for ax in axs[1])
for ax in axs[1]:
    ax.set_ylim(ymin, ymax * 1.1)
# Calculate and display integrals
shifts = (128.02, 125.43, 123.27, 113.23)
margin = 0.2
get_integs = lambda ds: np.array([ds.f1projp().integrate(peak=shift,
                                                         margin=margin,
                                                         mode="max")
                                  for shift in shifts])
ref_integs = get_integs(hmqc)
for ds, ax in zip(dss, axs[1]):
    integs = get_integs(ds)
    rel_integs = integs / ref_integs
    for i, shift, integ, rel_integ in apt.enzip(shifts, integs, rel_integs):
        voffset = (ymax*1.1 - ymin) * 0.05
        ax.text(x=shift, y=integ+voffset, s=f"{rel_integ:.1f}×",
                fontsize=8, ha='left' if i == 0 or i == 2 else 'center')

apt.label_axes_def(axs.T)
# apt.show()
apt.save(__file__)
