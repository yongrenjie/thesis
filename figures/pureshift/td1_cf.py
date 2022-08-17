"""
The data in td1_cf.out is generated using the script:
matlab_nmr_jy/research/optim_setup/td1_cf.m
"""

import matplotlib.pyplot as plt
import numpy as np
import penguins as pg
import aptenodytes as apt

apt.thesis()

data = np.loadtxt('td1_cf.out', delimiter=',')

td1_16 = data[0]
td1_8 = data[1]
td1_4 = data[2]

fig, axs = plt.subplots(1, 2, figsize=(6.5, 3.3))
axs[0].scatter(td1_16, td1_8, s=5, color=apt.PAL[0])
axs[0].set(xlabel=r'$f_\mathrm{diff,2}$ (16 chunks)',
           ylabel=r'$f_\mathrm{diff,2}$ (8 chunks)')
axins0 = axs[0].inset_axes([0.6, 0.1, 0.35, 0.35])
axins0.scatter(td1_16, td1_8, s=5, color=apt.PAL[0])
axins0.set(xlim=(0, 0.5), ylim=(0, 0.5))
axs[0].indicate_inset_zoom(axins0, edgecolor="black")
# find minimum by td1_16
min16 = np.argmin(td1_16)
axins0.scatter([td1_16[min16]], [td1_8[min16]], s=5, color=apt.PAL[2], zorder=1)

axs[1].scatter(td1_16, td1_4, s=5, color=apt.PAL[0])
axs[1].set(xlabel=r'$f_\mathrm{diff,2}$ (16 chunks)',
           ylabel=r'$f_\mathrm{diff,2}$ (4 chunks)')
axins1 = axs[1].inset_axes([0.6, 0.1, 0.35, 0.35])
axins1.scatter(td1_16, td1_4, s=5, color=apt.PAL[0])
axins1.set(xlim=(0, 0.5), ylim=(0, 0.5))
# find minimum by td1_4
min4 = np.argmin(td1_4)
axins1.scatter([td1_16[min4]], [td1_4[min4]], s=5, color=apt.PAL[3], zorder=1)
# find minimum by td1_16
min16 = np.argmin(td1_16)
axins1.scatter([td1_16[min16]], [td1_4[min16]], s=5, color=apt.PAL[2], zorder=1)

axs[1].indicate_inset_zoom(axins1, edgecolor="black")
for ax in axs:
    pg.style_axes(ax, 'plot')

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
