import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '211123-7c-psyche-sapphire'

dss = pg.read(p, [101004, 102004, 11004, 13004])

fig, axs = pg.subplots2d(2, 2, figsize=(6.5, 4), sharey=True)
for ds, ax in zip(dss, axs.flat):
    ds.stage(ax=ax, color='black', bounds=(0.4, 3.4))
    pg.mkplot()

apt.label_axes_def(axs)

# apt.show()
apt.save(__file__)
