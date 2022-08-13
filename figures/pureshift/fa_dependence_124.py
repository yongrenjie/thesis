"""
The data for this plot were simulated in Matlab: please see

matlab_nmr_jy/research/n_saltires/fa_dependence_124.m
"""

import matplotlib.pyplot as plt
import penguins as pg
import aptenodytes as apt
import numpy as np

apt.thesis()

data = np.loadtxt('fa_dependence_124.out', delimiter=',')

flip_angles = data[0]

saltire1_signals = data[1]
saltire1_artefacts = data[2]
saltire2_signals = data[3]
saltire2_artefacts = data[4]
saltire4_signals = data[5]
saltire4_artefacts = data[6]


fig, ax = plt.subplots(figsize=(6, 4))

bright = pg.color_palette('bright')
pastel = pg.color_palette('pastel')
ax.plot(flip_angles, saltire1_signals, color=bright[0], label='1 saltire')
ax.plot(flip_angles, saltire1_artefacts, color=pastel[0], linestyle='--')
ax.plot(flip_angles, saltire2_signals, color=bright[1], label='2 saltires')
ax.plot(flip_angles, saltire2_artefacts, color=pastel[1], linestyle='--')
ax.plot(flip_angles, saltire4_signals, color=bright[2], label='4 saltires')
ax.plot(flip_angles, saltire4_artefacts, color=pastel[2], linestyle='--')
ax.legend()
ax.set_xlabel('flip angle (°)')
ax.set_ylabel('state overlap')

ax.text(s='desired\n'+r'$I_{1{+}}I_{2\alpha} \,\to\, I_{1{-}}I_{2\alpha}$',
        x=32, y=0.145, ha='center')
ax.text(s='unwanted\n'+r'$I_{1{+}}I_{2\alpha} \,\to\, I_{1{-}}I_{2\beta}$',
        x=90, y=0.015, ha='center')

pg.style_axes(ax, 'plot')
# apt.show()
apt.save(__file__)
