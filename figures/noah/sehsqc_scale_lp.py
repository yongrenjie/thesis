"""POSTPROCESS WITH INKSCAPE because it's a real pain to make weird layouts
with MPL.

Steps:
(1) ungroup axes
(2) move axes (b) to x=241.882
(3) align the bottom edge of (a) to the bottom edge of (b)
(4) move axes (a) to x=91.15
(5) if necessary, move text labels to avoid collisions
"""

import numpy as np
from pathlib import Path
import penguins as pg
import aptenodytes as apt
import matplotlib.pyplot as plt

apt.thesis()

path = apt.nmrd() / "210310-7g-n15-sw1"
dss = [
    pg.read(path, 101001, 1),  # normal
    pg.read(path, 102001, 2),  # k = 2 LP
    pg.read(path, 103001, 2),  # k = 4 LP
    pg.read(path, 104001, 2),  # k = 8 LP
    pg.read(path, 105001, 2),  # SW * 2 LP
    pg.read(path, 106001, 2),  # SW * 4 LP
    pg.read(path, 107001, 2),  # SW * 8 LP
]
titles = [r"standard",
          r"$k$, 2×, +LP",
          r"$k$, 4×, +LP",
          r"$k$, 8×, +LP",
          r"SW, 2×, +LP",
          r"SW, 4×, +LP",
          r"SW, 8×, +LP"]

aqs = [f"{aq} ms" for aq in [60.1, 30.1, 15.0, 7.5, 30.1, 15.0, 7.5]]
aqeffs = [f"{aq} ms" for aq in [120.3, 60.1, 30.1, 15.0, 60.1, 30.1, 15.0]]
sws = [f"{sw} ppm" for sw in [30, 30, 30, 30, 60, 120, 240]]
td1s = [256, 128, 64, 32, 256, 256, 256]
nss = [2, 4, 8, 16, 2, 2, 2]
noise_levs = [1, np.sqrt(2), np.sqrt(4), np.sqrt(8),
              np.sqrt(2), np.sqrt(4), np.sqrt(8)]

fig, axs = pg.subplots2d(6, 3, height_ratios=[1, 0.45, 1, 0.45, 1, 0.45],
                         figsize=(6.5, 9.6))
axs[0][1].remove()
axs[0][2].remove()
axs[1][1].remove()
axs[1][2].remove()
axes_2d = [axs.flat[i] for i in (0, 6, 7, 8, 12, 13, 14)]
axes_1d = [axs.flat[i] for i in (3, 9, 10, 11, 15, 16, 17)]

f1b, f2b = "111..131", "7..9.3"

# Plot data.
for ds, ax, aq, aqeff, sw, td1, ns, title, noise in zip(dss, axes_2d, aqs, aqeffs,
                                                        sws, td1s, nss, titles,
                                                        noise_levs):
    ds.stage(ax, levels=5e3*noise, f1_bounds=f1b, f2_bounds=f2b)
    ax.text(x=0.18, y=0.98, s=title, transform=ax.transAxes, va="top")
    pg.mkplot(ax)
    pg.ymove(ax)
for ds, ax, noise in zip(dss, axes_1d, noise_levs):
    ds.f1projp().stage(ax, bounds="111..131", scale=1/noise, color="black")
    pg.mkplot(ax)
# Standardise ylims of projections.
ymin = min(ax.get_ylim()[0] for ax in axes_1d)
ymax = max(ax.get_ylim()[1] for ax in axes_1d)
for ax in axes_1d:
    ax.set_ylim(ymin, ymax * 1.1)

# Calculate and display integrals
shifts = (128.02, 125.43, 123.27, 113.23)
margin = 0.2
get_integs = lambda ds: np.array([ds.f1projp().integrate(peak=shift,
                                                         margin=margin,
                                                         mode="max")
                                  for shift in shifts])
ref_integs = get_integs(dss[0])
for ds, ax, noise in zip(dss[1:], axes_1d[1:], noise_levs[1:]):
    integs = get_integs(ds)
    rel_integs = integs / (ref_integs * noise)
    for i, shift, integ, rel_integ in apt.enzip(shifts, integs, rel_integs):
        voffset = (ymax*1.1 - ymin) * 0.05
        ax.text(x=shift, y=(integ/noise)+voffset, s=f"{rel_integ:.1f}×",
                fontsize=8, ha='left' if i == 0 or i == 2 else 'center')

apt.tl()
apt.label_axes_def(list(zip(axes_2d, axes_1d)))
# apt.show()
apt.save(__file__, svg=True)
