import penguins as pg
from matplotlib.patches import Rectangle
import aptenodytes as apt

apt.thesis()
path = apt.nmrd() / '211226-7a-hmbc-grad'

expnos = [i * 1000 + 1 for i in range(11, 17)]
dss = [pg.read(path, expno) for expno in expnos]
labels = ["Symm.",
          "Asymm. A, $\\alpha=1.67$",
          "Asymm. A, $\\alpha=0.6$",
          "Asymm. A, $\\alpha=0.3$",
          "Asymm. B",
          "Asymm. C",
          ]

fig, axs = pg.subplots2d(2, 3, figsize=(6.5, 5))
for i, ds, ax, label in apt.enzip(dss, axs.flat, labels):
    ds.stage(ax=ax, levels=300, f1_bounds="17..70", f2_bounds="0.4..2")
    xlabel = r'$^{1}$H (ppm)' if i in [3, 4, 5] else ''
    ylabel = r'$^{13}$C (ppm)' if i in [2, 5] else ''
    yticks = ['', '20', '40', '60'] if i in [2, 5] else []
    pg.mkplot(ax=ax, title=label, xlabel=xlabel, ylabel=ylabel)
    ax.set_yticklabels(yticks)
    pg.ymove(ax)
    if i == 1 or i == 4:
        r = Rectangle(xy=(0.53, 28), height=36, width=0.27, color='red', fill=None)
        ax.add_patch(r)

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
