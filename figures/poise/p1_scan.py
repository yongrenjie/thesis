import penguins as pg
import aptenodytes as apt
import numpy as np

apt.thesis()

p = apt.nmrd() / '200826-6f-scanp1'
datasets = [pg.read(p, expno, 1) for expno in range(1, 162)]
p1s = [ds["p1"] for ds in datasets]
cf = lambda ds: np.sum(np.abs(ds.real + 1j*ds.imag))
cfs = [cf(ds) for ds in datasets]
print(f"Smallest value of cf: {np.min(cfs)}")                # 33367794.51452232
print(f"Corresponding value of p1: {p1s[np.argmin(cfs)]}")   # 48.3

fig, ax = pg.subplots(figsize=(4.5, 3))
ax.plot(p1s, cfs)
ax.set(xlabel="p1 (µs)", ylabel=r"$f_\mathrm{minabsint}$")
pg.style_axes(ax, "plot")

# apt.show()
apt.save(__file__)
