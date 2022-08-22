import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '201020-7a-timereversal'

summed_spectrum = pg.read(p, 2000)
tse_psyche = pg.read(p, 1003)

fig, axs = pg.subplots(1, 2, figsize=(6.5, 2.5), sharey=True)

b = "1.55..2.60"
summed_spectrum.stage(axs[0], bounds=b, color='black')
tse_psyche.stage(axs[1], scale=7, bounds=b, color='black')
pg.mkplots(axs)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
