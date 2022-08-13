import penguins as pg
import aptenodytes as apt
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

apt.thesis()
p = apt.nmrd() / 'jy-190823-chirpoptnm2'

target = pg.read(p, 1)
saltire = pg.read(p, 14)
bad_optimum = pg.read(p, 68)


bounds = (0, 9.5)
fig, ax = pg.subplots(figsize=(4, 3))
target.stage(ax=ax, scale=1/np.linalg.norm(target.real), bounds=bounds)
saltire.stage(ax=ax, scale=1/np.linalg.norm(saltire.real), bounds=bounds)
bad_optimum.stage(ax=ax, scale=1/np.linalg.norm(bad_optimum.real), bounds=bounds)
pg.mkplot(ax, stacked=True)

def magnification(ds):
    plot_scaled_up_by = np.linalg.norm(target.real)/np.linalg.norm(ds.real)
    scale = plot_scaled_up_by * (ds['ns'] / target['ns']) * (ds['rg'] / target['rg'])
    return scale

def cf(ds, cf_type=1):
    r = ds.real
    i = ds.imag
    t = target.real

    b = (4.72, 5.92)
    rb = ds.proc_data(bounds=b)
    tb = target.proc_data(bounds=b)

    if cf_type == 1:    # f_phase
        return np.var(np.arctan(r / np.abs(i)))
    elif cf_type == 2:   # f_diff whole spectrum
        return np.linalg.norm(r/np.linalg.norm(r) - t/np.linalg.norm(t))
    elif cf_type == 3:
        return np.linalg.norm(rb/np.linalg.norm(rb) - tb/np.linalg.norm(tb))


cf_type = 3
ax.text(s=f"cf = {cf(saltire, cf_type):.3f}\n({magnification(saltire):.1f}×)",
        x=0.05, y=ax.prop.voffsets[1]+0.005, transform=ax.get_yaxis_transform(),
        color=ax.prop.colors[1], va="bottom")
ax.text(s=f"cf = {cf(bad_optimum, cf_type):.3f}\n({magnification(bad_optimum):.1f}×)",
        x=0.05, y=ax.prop.voffsets[2]+0.005, transform=ax.get_yaxis_transform(),
        color=ax.prop.colors[2], va="bottom")
apt.show()
