import numpy as np
import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / "HSQC_OptScan"

peaks = [(130.50, 7.63), (120.43, 7.54), (130.03, 7.38), (117.23, 7.20)]
peak_labels = [rf"$(\delta_1, \delta_2) = ({peak[0]:.2f}, {peak[1]:.2f})$" for peak in peaks]

dss = [pg.read(p, expno, 1) for expno in range(101, 134)]
cnst3s = [ds["cnst3"] for ds in dss]

integrals = np.zeros((len(peaks), len(dss)))
for i, peak in enumerate(peaks):
    for j, ds in enumerate(dss):
        integrals[i, j] = ds.integrate(peak=peak, margin=(1.5, 0.06), mode="max")

# print(integrals)
avg_integrals = np.sum(integrals, axis=0) / 4

fig, ax = pg.subplots(figsize=(6, 4))
for peak, ints in zip(peaks, integrals):
    ax.plot(cnst3s, ints, linestyle="--", linewidth=0.8)
ax.plot(cnst3s, avg_integrals, color="black", linewidth=1.5)

ax.legend([*peak_labels, "average"], ncol=2)
ax.set(xlabel=r"$J_\mathrm{eff}$ (Hz)",
       ylabel="crosspeak intensity (au)",
       )
pg.style_axes(ax, "plot")

# apt.show()
apt.save(__file__)
