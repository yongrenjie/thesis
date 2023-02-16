import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '211123-7c-psyche-sapphire'

dss = pg.read(p, [1, 21004])

fig, axs = pg.subplots(2, 1, figsize=(5, 4))

for ds, ax in zip(dss, axs):
    ds.stage(ax, bounds="4.6..6", color="black")
    pg.mkplot(ax)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
