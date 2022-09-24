from pathlib import Path
import numpy as np
import penguins as pg
import aptenodytes as apt
from aptenodytes import Andrographolide as Andro
import matplotlib.pyplot as plt

apt.thesis()

path = apt.nmrd() / "201010-7a-hsqctocsy"

# Read reference datasets and get reference intensities
ref_s, ref_c = [pg.read(path, expno) for expno in (1001, 1002)]
ref_s_ints = Andro.hsqc.integrate(ref_s)
ref_c_ints = Andro.cosy.integrate(ref_c)

# Read in datasets of interest
mfa_s1, mfa_s2, mfa_c = [pg.read(path, expno) for expno in (6001, 6002, 6003)]
noah_s1 = [pg.read(path, expno * 1000 + 1) for expno in range(11, 18)]
noah_s2 = [pg.read(path, expno * 1000 + 2) for expno in range(11, 18)]
noah_c = [pg.read(path, expno * 1000 + 3) for expno in range(11, 18)]

# seHSQC in slot 2
noah_sps1 = [pg.read(path, expno * 1000 + 1) for expno in range(31, 38)]
noah_sps2 = [pg.read(path, expno * 1000 + 2) for expno in range(31, 38)]
noah_spc = [pg.read(path, expno * 1000 + 3) for expno in range(31, 38)]

# Calculate intensities (averaged over all peaks) for datasets of interest
get_rel_s_ints = lambda ds: np.mean(Andro.hsqc.integrate(ds) / ref_s_ints)
get_rel_c_ints = lambda ds: np.mean(Andro.cosy.integrate(ds) / ref_c_ints)
mfa_s1_int = get_rel_s_ints(mfa_s1)
mfa_s2_int = get_rel_s_ints(mfa_s2)
mfa_c_int = get_rel_c_ints(mfa_c)
noah_s1_ints = list(map(get_rel_s_ints, noah_s1))
noah_s2_ints = list(map(get_rel_s_ints, noah_s2))
noah_c_ints = list(map(get_rel_c_ints, noah_c))
noah_sps1_ints = list(map(get_rel_s_ints, noah_sps1))
noah_sps2_ints = list(map(get_rel_s_ints, noah_sps2))
noah_spc_ints = list(map(get_rel_c_ints, noah_spc))

# Get values of cnst32
cnst32s = [ds["cnst32"] for ds in noah_c]

# Plot them. This code is modified from 201007 lab book.
fig, axs = pg.subplots2d(1, 3, sharey=True, width_ratios=[4, 4, 0.5],
                         figsize=(6.5, 3.2))
# Axes #2 and #3 - NOAH intensities, but with MFA dotted lines
for (ax, s1_ints, s2_ints,
     c_ints, label1, label2) in zip(axs[0:2],
                                    [noah_s1_ints, noah_sps1_ints],
                                    [noah_s2_ints, noah_sps2_ints],
                                    [noah_c_ints, noah_spc_ints],
                                    ["HSQC #1", "HSQC"],
                                    ["HSQC #2", "seHSQC"]):
    # Plot NOAH intensities
    for i, c, m in zip((s1_ints, s2_ints, c_ints), apt.PAL, "osx"):
        ax.plot(cnst32s, i, marker=m, color=c)
    for i, c in zip((mfa_s1_int, mfa_s2_int, mfa_c_int), apt.PAL):
        ax.axhline(y=i, color=c, linestyle="--", linewidth=0.5)
    # Twiddle with axes properties.
    ax.set(xlabel="$f$")
    ax.legend([label1, label2, "COSY"], loc="lower right")
    ax.invert_xaxis()

# Axes #1 - MFA intensities
# Plot MFA intensities and line to guide the eye
for i, c, m in zip((mfa_s1_int, mfa_s2_int, mfa_c_int), apt.PAL, "osx"):
    axs[2].plot(1, i, marker=m, color=c)
    axs[2].axhline(y=i, color=c, linestyle="--", linewidth=0.5)
    axs[2].set(xticks=[1], xticklabels=[])
    axs[2].set(ylabel="relative intensity",
               ylim=(-0.05, 1.15))

for ax in axs.flat:
    ax.label_outer()
    pg.style_axes(ax, "plot")

axs[0].text(x=0.10, y=0.977, va='top', ha='left',
            s=r'NOAH-3 $\rm SSC^c$', transform=axs[0].transAxes)
axs[1].text(x=0.10, y=0.977, va='top', ha='left',
            s=r'NOAH-3 $\rm SS^{+}C^c$', transform=axs[1].transAxes)

apt.label_axes_def(axs[0:2])
apt.label_axes_def([axs[2]], start=3, x=0.15)
# apt.show()
apt.save(__file__)
