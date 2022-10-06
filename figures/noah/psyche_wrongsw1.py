import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '211123-7c-psyche-sapphire'

dss = pg.read(p, [101004, 102004, 11004, 13004, 21004, 23004])

labels = [
    'no SAPPHIRE, 50 Hz, misset chunk size',
    'SAPPHIRE, 50 Hz, misset chunk size',
    'no SAPPHIRE, 50 Hz',
    'SAPPHIRE, 50 Hz',
    'no SAPPHIRE, 25 Hz',
    'SAPPHIRE, 25 Hz',
]

fig, axs = pg.subplots2d(3, 2, figsize=(6.5, 6))
for ds, ax, label in zip(dss, axs.flat, labels):
    ds.stage(ax=ax, color='black', bounds=(0.4, 3.4), linewidth=0.8)
    ax.text(x=0.10, y=0.975, s=label, ha='left', va='top',
            transform=ax.transAxes)
    pg.mkplot()

ymin = min(ax.get_ylim()[0] for ax in axs.flat)
ymax = max(ax.get_ylim()[1] for ax in axs.flat)
for ax in axs.flat:
    ax.set_ylim((ymin, ymax * 1.2))

apt.label_axes_def(axs)

# apt.show()
apt.save(__file__)
