import penguins as pg
import aptenodytes as apt
from matplotlib.patches import Rectangle

apt.thesis()
p = apt.nmrd() / '201115-7a-c13-sehsqc-full'

sehsqc1 = pg.read(p, 21001)
sehsqc2 = pg.read(p, 23001)

fig, axs = pg.subplots(1, 2, figsize=(5, 2.4))
sehsqc1.stage(axs[0], f1_bounds="18..60", f2_bounds="1..2.7", levels=5e3)
sehsqc2.stage(axs[1], f1_bounds="18..60", f2_bounds="1..2.7", levels=5e3)
pg.mkplots(axs)
pg.ymove(axs)

# highlight artefacts
axs[1].add_patch(Rectangle(xy=(1.16, 22), width=0.12, height=8,
                           color='red', fill=None, transform=axs[1].transData))
axs[1].add_patch(Rectangle(xy=(1.28, 53.2), width=0.16, height=3,
                           color='red', fill=None, transform=axs[1].transData))
axs[1].add_patch(Rectangle(xy=(1.04, 51.2), width=0.09, height=3.5,
                           color='red', fill=None, transform=axs[1].transData))
axs[1].add_patch(Rectangle(xy=(2.44, 54.5), width=0.08, height=3,
                           color='red', fill=None, transform=axs[1].transData))
axs[1].add_patch(Rectangle(xy=(1.83, 22.7), width=0.08, height=3,
                           color='red', fill=None, transform=axs[1].transData))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
