import numpy as np
import matplotlib.pyplot as plt
import penguins as pg
import aptenodytes as apt
from pathlib import Path

apt.thesis()
z_to_y = np.loadtxt(Path(__file__).parent / 'spv1_evaluate_200us_99.99_z.out',
                    delimiter=',')
y_to_x = np.loadtxt(Path(__file__).parent / 'spv1_evaluate_200us_99.99_y.out',
                    delimiter=',')
labels = ['$x$-magnetisation', '$y$-magnetisation', '$z$-magnetisation',
          '$xy$-magnetisation', 'phases (°)']

fig, axs = plt.subplots(5, 2, figsize=(6, 4), sharex=True)
ylims = [(-0.3, 1.8),
         (-0.3, 1.8),
         (-0.3, 0.3),
         (-0.3, 1.8),
         (-30, 180),
         ]

for i, label, ylim, ax_row in apt.enzip(labels, ylims, axs):
    for data, clr, ax in zip([z_to_y, y_to_x], apt.PAL, ax_row):
        ax.plot(data[0], data[i + 1], color=clr)
        ax.set(xlabel='offset (Hz)', ylim=ylim)
        ax.invert_xaxis()
        ax.label_outer()
        pg.style_axes(ax, 'plot')
        ax.text(x=0.09, y=0.95, s=label, va='top', transform=ax.transAxes)
        if i == 4:
            ax.set_yticks([0, 90])

apt.label_axes_def([row[0] for row in axs], x=0.01, y=0.95)
apt.label_axes_def([row[1] for row in axs], start=6, x=0.01, y=0.95)
# apt.show()
apt.save(__file__)
