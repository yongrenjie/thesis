import penguins as pg
import aptenodytes as apt
import numpy as np

apt.thesis()
p = apt.nmrd() / '201017-7g-n15-sehsqc-full'
hmqc = pg.read(p, 12002)
hsqc = pg.read(p, 22002)
sehsqc1 = pg.read(p, 32002)
sehsqc2 = pg.read(p, 42002)
dss = [hsqc, sehsqc1, sehsqc2]
titles = ['HSQC', 'seHSQC1', 'seHSQC2']

fig, axs = pg.subplots2d(3, 3, figsize=(6.5, 5.6),
                         height_ratios=[0.9, 0.6, 1.4])
f1b, f2b = "16..62", "0.6..5.0"

# Plot 2D data
for ds, ax, title in zip(dss, axs[0], titles):
    ds.stage(ax=ax, levels=1e4, f1_bounds=f1b, f2_bounds=f2b)
    pg.mkplot(ax)
    ax.text(s=title, x=0.2, y=0.98, ha='left', va='top',
            transform=ax.transAxes)
    pg.ymove(ax)
# Plot projections
for ds, ax in zip(dss, axs[1]):
    ds.f1projp().stage(ax, bounds="16..62", color='black')
    pg.mkplot(ax)
# Standardise ylims of projections.
ymin = min(ax.get_ylim()[0] for ax in axs[1])
ymax = max(ax.get_ylim()[1] for ax in axs[1])
for ax in axs[1]:
    ax.set_ylim(ymin, ymax * 1.1)
# Stripplots
for ds, ax in zip(dss, axs[2]):
    apt.generic_stripplot(experiment=apt.Gramicidin.hsqc,
                          datasets=[ds],
                          ref_dataset=hmqc,
                          expt_labels=[''],
                          xlabel='', ylabel='',
                          palette=[pg.color_palette('dark')[7]],
                          ax=ax, legend=False)
    ax.set(ylim=(0, 1.2))
axs[2][0].set(ylabel="relative intensity")
apt.tl()

apt.label_axes_def(axs.T)
# apt.show()
apt.save(__file__)
