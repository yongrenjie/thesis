from pathlib import Path
import numpy as np
import penguins as pg
import aptenodytes as apt
from aptenodytes import Andrographolide as Andro
import matplotlib.pyplot as plt

apt.thesis()

# Can also use 201206-7a-hsqct-full, the results are the same
# but 210126 dataset includes seHSQC-TOCSY
path = apt.nmrd() / "210126-7a-hsqct-full"

ref_noah_sc_expno = 3
ssc_expnos = range(11, 19)
sspc_expnos = range(19, 27)
stsc_expnos = range(27, 35)
stspc_expnos = range(35, 43)


# Read reference datasets and get reference intensities
ref_s, ref_c = [pg.read(path, expno)
                for expno in (ref_noah_sc_expno * 1000 + 1,
                              ref_noah_sc_expno * 1000 + 2)]
ref_s_ints = Andro.hsqc.integrate(ref_s)
ref_c_ints = Andro.cosy.integrate(ref_c)

# Read in datasets of interest
noah_ssc_s = [pg.read(path, expno * 1000 + 2) for expno in ssc_expnos]
noah_ssc_c = [pg.read(path, expno * 1000 + 3) for expno in ssc_expnos]
noah_stsc_s = [pg.read(path, expno * 1000 + 2) for expno in stsc_expnos]
noah_stsc_c = [pg.read(path, expno * 1000 + 3) for expno in stsc_expnos]

# seHSQC in slot 2
noah_sspc_sp = [pg.read(path, expno * 1000 + 2) for expno in sspc_expnos]
noah_sspc_c = [pg.read(path, expno * 1000 + 3) for expno in sspc_expnos]
noah_stspc_sp = [pg.read(path, expno * 1000 + 2) for expno in stspc_expnos]
noah_stspc_c = [pg.read(path, expno * 1000 + 3) for expno in stspc_expnos]

# seHSQC-TOCSY
stpspc_sp = pg.read(path, 43002)
stpspc_c = pg.read(path, 43003)

# Calculate intensities (averaged over all peaks) for datasets of interest
get_rel_s_ints = lambda ds: np.mean(Andro.hsqc.integrate(ds) / ref_s_ints)
get_rel_c_ints = lambda ds: np.mean(Andro.cosy.integrate(ds) / ref_c_ints)
mkarray = lambda fn, dss: np.array(list(map(fn, dss)))

noah_ssc_s_ints = mkarray(get_rel_s_ints, noah_ssc_s)
noah_ssc_c_ints = mkarray(get_rel_c_ints, noah_ssc_c)
noah_stsc_s_ints = mkarray(get_rel_s_ints, noah_stsc_s)
noah_stsc_c_ints = mkarray(get_rel_c_ints, noah_stsc_c)
noah_sspc_sp_ints = mkarray(get_rel_s_ints, noah_sspc_sp)
noah_sspc_c_ints = mkarray(get_rel_c_ints, noah_sspc_c)
noah_stspc_sp_ints = mkarray(get_rel_s_ints, noah_stspc_sp)
noah_stspc_c_ints = mkarray(get_rel_c_ints, noah_stspc_c)
stp_s2_int = get_rel_s_ints(stpspc_sp)
stp_c_int = get_rel_c_ints(stpspc_c)

# Get values of cnst32
cnst32s = [ds["cnst32"] for ds in noah_ssc_s]

# Plot them.
fig, axs = pg.subplots2d(1, 3, sharey=True, width_ratios=[4, 4, 0.5],
                         figsize=(6.5, 3.2))
pastel = pg.color_palette("pastel")
for (ax,
     s1_ints, s2_ints,
     c1_ints, c2_ints,
     label2) in zip(axs,
                    [noah_ssc_s_ints, noah_sspc_sp_ints],
                    [noah_stsc_s_ints, noah_stspc_sp_ints],
                    [noah_ssc_c_ints, noah_sspc_c_ints],
                    [noah_stsc_c_ints, noah_stspc_c_ints],
                    ["HSQC #2", "seHSQC"]):
    # Plot NOAH intensities
    ax.plot(cnst32s, s1_ints, linestyle="--", color=pastel[1], marker="s")
    ax.plot(cnst32s, s2_ints, color=apt.PAL[1], marker="s", label=label2)
    ax.plot(cnst32s, c1_ints, linestyle="--", color=pastel[2], marker="x")
    ax.plot(cnst32s, c2_ints, color=apt.PAL[2], marker="x", label="COSY")
    # Twiddle with axes properties.
    ax.set(xlabel="$f$",
           ylabel="relative intensity",
           ylim=(-0.05, 1.15))
    ax.legend(loc='lower right')
    ax.invert_xaxis()

for i, c, m in zip((stp_s2_int, stp_c_int), apt.PAL[1:], "sx"):
    axs[2].plot(1, i, marker=m, color=c)
    axs[2].set(xticks=[1], xticklabels=[])
    axs[2].set(ylabel="relative intensity",
               ylim=(-0.05, 1.15))
    for ax in axs:
        for i, c in zip((stp_s2_int, stp_c_int), apt.PAL[1:]):
            ax.axhline(y=i, color=c, linestyle=":", linewidth=1, zorder=-1)

for ax in axs:
    ax.label_outer()
    pg.style_axes(ax, "plot")


axs[0].text(x=0.10, y=0.98, va='top', ha='left',
            s=r'NOAH-3 $\rm S^TSC^c$'+'\n'+r'(dashed: $\rm SSC^c$)', transform=axs[0].transAxes)
axs[1].text(x=0.10, y=0.98, va='top', ha='left',
            s=r'NOAH-3 $\rm S^TS^{+}C^c$'+'\n'+r'(dashed: $\rm SS^{+}C^c$)', transform=axs[1].transAxes)

apt.label_axes_def(axs[0:2])
apt.label_axes_def([axs[2]], start=3, x=0.15)
# apt.show()
apt.save(__file__)
