import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / "DOSY_Opt"

# read data from increment 1 through 20
incrs = [pg.read(p, e, 1) for e in range(1001, 1021)]
peaks = ["4.32..4.48",   # not OH
         "5.54..5.84",   # OH
         ]
gpzs = [10.0000, 19.8883, 26.2886, 31.4108, 35.8076, 39.7206, 43.2813,
        46.5706, 49.6423, 52.5348, 55.2761, 57.8878, 60.3866, 62.7861,
        65.0971, 67.3289, 69.4890, 71.5840, 73.6194, 75.6000]  # percentage
MAX_GRAD = 0.657   # T/m on the 600
gpzs = np.array([gpz * (MAX_GRAD / 100) for gpz in gpzs])
ints = [[incr.integrate(bounds=peak) for incr in incrs] for peak in peaks]

# plot the intensities
labels = ("4.4 ppm (CH)", "5.7 ppm (OH)")
markers = ('o', 'x')
fig, ax = plt.subplots(figsize=(6, 4))
for ins, lbl, mkr, clr in zip(ints, labels, markers, apt.PAL):
    ax.scatter(gpzs, ins, s=12, marker=mkr, label=lbl, color=clr, linewidths=1)
    ax.text(x=gpzs[-1]+0.01, y=ins[-1]-1e5, s=f"({round(100*ins[-1]/ins[0])}%)",
            horizontalalignment="left", verticalalignment="center",
            color=clr, fontweight="semibold")
ax.set(xlabel="gradient amplitude (T/m)",
       ylabel="intensity (au)")

ax.legend()

# perform fitting and plot those
import numpy as np
from scipy.optimize import curve_fit

def stanner(g, I_0, D):
    gamma = 42576080  # gyrom. ratio of 1H (Hz / T)
    tau = 0.001224    # value of tau (s)
    Delta = 0.1       # big Delta, diffusion delay
    delta = 0.002     # little delta, gradient duration
    alpha = 0.2       # imbalance factor
    # dosytimecubed (s^3)
    cnst18 = delta * delta * (Delta
                              - (delta * (5 - 3*alpha*alpha)/16)
                              - (tau * (1 - alpha*alpha)/2))
    return I_0 * np.exp(-D * (g ** 2) * (gamma ** 2) * cnst18)

for ins, pastel_clr in zip(ints, pg.color_palette('pastel')):
    (I_0, D), pcov = curve_fit(f=stanner, xdata=gpzs, ydata=ins, p0=[1e8, 1e-10])
    new_xs = np.linspace(gpzs[0], gpzs[-1], 1000)
    new_ys = stanner(new_xs, I_0, D)
    ax.plot(new_xs, new_ys, color=pastel_clr, linestyle="--", zorder=0)
    print(f'D = {D} ± {np.sqrt(np.diag(pcov))[1]}')

xmin, xmax = ax.get_xlim()
ax.set_xlim(xmin, xmax + 0.032)

pg.style_axes(ax, "plot")


# apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
