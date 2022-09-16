import numpy as np
import penguins as pg
import matplotlib.pyplot as plt
from pathlib import Path
import aptenodytes as apt

apt.thesis()
data = np.loadtxt(Path(__file__).parent / 'exsculpt_profile.out',
                  delimiter=',', dtype=complex)

fig, axs = plt.subplots(1, 2, figsize=(6, 1.8), sharey=True)

axs[0].plot(np.real(data[0]), np.real(data[1]), color='black', linewidth=1)
axs[0].set(xlabel="$^1$H (Hz)")
axs[1].plot(np.real(data[0]), np.real(data[2]), color='black', linewidth=1)
axs[1].set(xlabel="$^1$H (Hz)")

for ax in axs:
    ax.invert_xaxis()
    pg.style_axes(ax, '1d')

apt.label_axes_def(axs, x=-0.01)
# apt.show()
apt.save(__file__)
