import penguins as pg
import numpy as np
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / 'NOESY_OptScan'
dss = [pg.read(p, expno, 1) for expno in (104, 135)]

fig, axs = pg.subplots(1, 2, figsize=(5.3, 2.6))
for ds, ax, char in zip(dss, axs, "ab"):
    ds.stage(ax=ax, levels=1e5, f1_bounds="7.1..7.7", f2_bounds="7.1..7.7")
    pg.mkplot(ax)
    pg.ymove(ax)

# show sensitivity increases
peaks = [(7.63, 7.38), (7.38, 7.19),
         (7.38, 7.63), (7.19, 7.38)]
for f1, f2 in peaks:
    int_unopt = dss[0].integrate(peak=(f1, f2), margin=(0.02, 0.02),
                                 mode="min")
    int_opt = dss[1].integrate(peak=(f1, f2), margin=(0.02, 0.02),
                               mode="min")
    sens_enhancement = 100 * (int_opt - int_unopt) / int_unopt
    axs[1].text(x=f2, y=f1 - 0.05, s=f"+{sens_enhancement:.0f}%",
                ha='center')

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
