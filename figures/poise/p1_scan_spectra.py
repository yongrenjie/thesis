import penguins as pg
import aptenodytes as apt
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

apt.thesis()

path = apt.nmrd() / '200826-6f-scanp1'

separation = 0.1

fig, ax = pg.subplots(figsize=(5.5, 3))
for expno in range(1, 162):
    ds = pg.read(path, expno)
    s = 0.08
    p = 3.3643
    spectrum = ds.proc_data(bounds=(p - s, p + s))
    npoints = spectrum.size
    xaxis = np.linspace(ds['p1'] - (separation / 2),
                        ds['p1'] + (separation / 2),
                        npoints)
    ax.plot(xaxis, spectrum, color='black', linewidth=0.5)
ax.set(xlabel=r"$\tau_\mathrm{p}$ (µs)")
pg.style_axes(ax, '1d')

# apt.show()
apt.save(__file__)
