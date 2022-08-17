import penguins as pg
import aptenodytes as apt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from pathlib import Path

apt.thesis()
p = apt.nmrd() / 'jy-190823-chirpoptnm2'

target = pg.read(p, 1)
saltire = pg.read(p, 14)
bad_optimum = pg.read(p, 68)

bounds = (0, 9.5)
fig, ax = pg.subplots(figsize=(6.5, 3.5))
target.stage(ax=ax, scale=1/np.linalg.norm(target.real), bounds=bounds)
saltire.stage(ax=ax, scale=1/np.linalg.norm(saltire.real), bounds=bounds)
bad_optimum.stage(ax=ax, scale=1/np.linalg.norm(bad_optimum.real), bounds=bounds)
pg.mkplot(ax, stacked=True)

def magnification(ds):
    plot_scaled_up_by = np.linalg.norm(target.real)/np.linalg.norm(ds.real)
    scale = plot_scaled_up_by * (ds['ns'] / target['ns']) * (ds['rg'] / target['rg'])
    return scale

def cf(ds, cf_type='diff'):
    r = ds.real
    i = ds.imag
    t = target.real

    b = (4.72, 5.92)
    rb = ds.proc_data(bounds=b)
    tb = target.proc_data(bounds=b)

    if cf_type == 'phase':    # f_phase
        return np.var(np.arctan(r / np.abs(i)))
    elif cf_type == 'diff':   # f_diff whole spectrum
        return np.linalg.norm(r/np.linalg.norm(r) - t/np.linalg.norm(t))
    elif cf_type == 'diff_ha_only':   # f_diff Ha region only
        return np.linalg.norm(rb/np.linalg.norm(rb) - tb/np.linalg.norm(tb))

ax.text(s=f"$f_\\mathrm{{diff}}$ = {cf(saltire, 'diff'):.2f}",
        x=0.1, y=0.63, transform=ax.transAxes, color=ax.prop.colors[1], va="top")
ax.text(s=f"$f_\\mathrm{{diff}}$ = {cf(bad_optimum, 'diff'):.2f}",
        x=0.1, y=0.96, transform=ax.transAxes, color=ax.prop.colors[2], va="top")
ax.text(s=f"({magnification(saltire):.1f}×)",
        transform=ax.get_yaxis_transform(),
        x=0.05, y=ax.prop.voffsets[1]+1e-2, color=ax.prop.colors[1])
ax.text(s=f"({magnification(bad_optimum):.1f}×)",
        transform=ax.get_yaxis_transform(),
        x=0.05, y=ax.prop.voffsets[2]+1e-2, color=ax.prop.colors[2])

# draw the rectangle
ax.add_patch(Rectangle(xy=(4.72, 0.02), width=(5.94-4.72), height=0.97,
                       linestyle="--", linewidth=1.5,
                       transform=ax.get_xaxis_transform(), ec="#888888", fc="none"))
ax.text(s=f"$f'_\\mathrm{{diff}}$ = {cf(saltire, 'diff_ha_only'):.2f}",
        x=0.392, y=0.63, transform=ax.transAxes, color=ax.prop.colors[1], va="top")
ax.text(s=f"$f'_\\mathrm{{diff}}$ = {cf(bad_optimum, 'diff_ha_only'):.2f}",
        x=0.392, y=0.96, transform=ax.transAxes, color=ax.prop.colors[2], va="top")


# manually label since these aren't subplots :(
ax.text(s="(a)", fontweight="semibold", fontsize=10, x=0.05, y=0.30,
        transform=ax.transAxes, va='top')
ax.text(s="(b)", fontweight="semibold", fontsize=10, x=0.05, y=0.63,
        transform=ax.transAxes, va='top')
ax.text(s="(c)", fontweight="semibold", fontsize=10, x=0.05, y=0.96,
        transform=ax.transAxes, va='top')

apt.tl()
# apt.show()
apt.save(__file__)
