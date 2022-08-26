import penguins as pg
import numpy as np
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / 'NOESY_OptScan'
peaks = [(7.63, 7.38), (7.38, 7.63), (7.38, 7.19), (7.19, 7.38)]
peak_labels = [rf"$(\delta_1, \delta_2) = {peak}$" for peak in peaks]

dss = [pg.read(p, expno, 1) for expno in range(101, 160)]
d8s = [ds["d8"] for ds in dss]

integrals = np.zeros((len(peaks), len(dss)))
for i, peak in enumerate(peaks):
    for j, ds in enumerate(dss):
        integrals[i, j] = ds.integrate(peak=peak, margin=(0.06, 0.06),
                                       mode="min") / 1e5

# print(integrals)
avg_integrals = np.mean(integrals, axis=0)
for i in [3, 34]:
    print(f"avg_integral at mixing time {d8s[i]} s = {avg_integrals[i]}")

fig, ax = pg.subplots(figsize=(6, 4))
for peak, ints in zip(peaks, integrals):
    ax.plot(d8s, ints, linestyle="--", linewidth=0.8)
ax.plot(d8s, avg_integrals, color="black", linewidth=1.5)

ax.legend([*peak_labels, "average"], ncol=3)
ax.set(xlabel="mixing time (s)",
       ylabel="crosspeak intensity (au)",
       )
pg.style_axes(ax, "plot")

# apt.show()
apt.save(__file__)
