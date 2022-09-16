import penguins as pg
import aptenodytes as apt
import numpy as np

apt.thesis()
path = apt.nmrd() / "201014-7s-solvsupp"

s_dss = [pg.read(path, expno) for expno in range(101, 160)]
spv1_dss = [pg.read(path, expno) for expno in range(301, 360)]
spv2_dss = [pg.read(path, expno) for expno in range(401, 460)]
hoffsets = [ds["O1P"] for ds in s_dss]
separation = hoffsets[1] - hoffsets[0]
titles = ["HSQC", "seHSQC1", "seHSQC2"]

fig, axs = pg.subplots(3, 1, figsize=(5.5, 5), sharey=True)
for ax, dss, title in zip(axs.flat, [s_dss, spv1_dss, spv2_dss], titles):
    for ds in dss:
        spectrum = ds.mc().proc_data(bounds="4.6..4.8")
        npoints = spectrum.size
        xaxis = np.linspace(4.7 - (ds['o1p'] - (separation / 2)),
                            4.7 - (ds['o1p'] + (separation / 2)),
                            npoints)
        ax.plot(xaxis, spectrum, color='black', linewidth=0.7)
    pg.style_axes(ax, '1d')
    ax.set_xlabel('chemical shift of water relative to transmitter offset (ppm)')
    ax.label_outer()
    ax.invert_xaxis()

    ax.text(s=title, x=0.05, y=0.96, ha='left', va='top',
            transform=ax.transAxes)

apt.label_axes_def(axs, x=0.005, y=0.96)
apt.tl()
# apt.show()
apt.save(__file__)
