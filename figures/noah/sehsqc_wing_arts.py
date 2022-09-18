import penguins as pg
import aptenodytes as apt
from matplotlib.patches import Rectangle

apt.thesis()
p = apt.nmrd() / '201115-7a-c13-sehsqc-full'

two_grads = pg.read(p, 23002)
one_grad = pg.read(p, 25002)

fig, axs = pg.subplots(1, 2, figsize=(5, 2.4))
b1 = "0.06..2.7"
b2 = "0.5..2.7"
two_grads.stage(axs[0], f1_bounds=b1, f2_bounds=b2, levels=1.4e5)
one_grad.stage(axs[1], f1_bounds=b1, f2_bounds=b2, levels=1.4e5)
pg.mkplots(axs)
pg.ymove(axs)

axs[1].add_patch(Rectangle(xy=(0.566, 0.089), width=0.2, height=1.09,
                           color='grey', linestyle='--', fill=None,
                           transform=axs[1].transData))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
