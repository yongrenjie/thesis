import penguins as pg
import aptenodytes as apt
import numpy as np

apt.thesis()

p = apt.nmrd() / 'jy-190907-FAscan'

# Reference dataset
ref_ds = pg.read(p, 1)

# Cost functions
def f_phase(ds):
    return np.var(np.arctan(ds.real / np.abs(ds.imag)))

def f_diff(ds):
    return np.linalg.norm((ds.real / np.linalg.norm(ds.real))
                          - (ref_ds.real / np.linalg.norm(ref_ds.real)))

# Process data
flip_angles = list(range(4, 52, 2))

phase_means = []
phase_stdevs = []
diff_means = []
diff_stdevs = []

for i, flip_angle in enumerate(flip_angles):
    # Read in the datasets with the given flip angles.
    expnos = range(2 + (i * 5), 7 + (i * 5))
    dss = pg.read(p, expnos)

    # Make sure that they're really correct (just in case)
    for ds in dss:
        assert int(ds['cnst20']) == flip_angle

    # Calculate cost function means and stdevs
    f_phases = np.array([f_phase(ds) for ds in dss])
    f_diffs = np.array([f_diff(ds) for ds in dss])
    phase_means.append(np.mean(f_phases))
    phase_stdevs.append(np.std(f_phases))
    diff_means.append(np.mean(f_diffs))
    diff_stdevs.append(np.std(f_diffs))

fig, ax = pg.subplots(figsize=(5, 3))
bright = pg.color_palette('bright')
ax.plot(flip_angles, phase_means, marker='o',
        label=r"$f_\mathrm{phase}$", color=bright[0])
ax.plot(flip_angles, diff_means, marker='o',
        label=r"$f_\mathrm{diff}$", color=bright[1])
# Can do with error bars if desired, but they're pretty small:
# ax.errorbar(x=flip_angles, y=phase_means, yerr=phase_stdevs,
#             label=r"$f_\text{phase}$", color=bright[0])
# ax.errorbar(x=flip_angles, y=diff_means, yerr=diff_stdevs,
#             label=r"$f_\text{diff}$", color=bright[1])
ax.set(xlabel='flip angle (°)', ylabel='cost function value')
ax.legend()

pg.style_axes(ax, 'plot')
# apt.show()
apt.save(__file__)
