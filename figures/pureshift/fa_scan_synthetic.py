import penguins as pg
import aptenodytes as apt
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import default_rng

apt.thesis()

rng = default_rng(seed=1815)

freqs = np.linspace(-4, 4, 200)
relaxation = 0.05   # 1/T2

# Generate synthetic signals
def absorption(offset, snr):
    if snr == np.inf:
        noise = np.zeros(100)
    else:
        noise = rng.normal(scale=(20/snr), size=200)
    return relaxation/(((freqs - offset) ** 2) + (relaxation ** 2)) + noise
def dispersion(offset, snr):
    if snr == np.inf:
        noise = np.zeros(200)
    else:
        noise = rng.normal(scale=(20/snr), size=200)
    return -(freqs - offset)/(((freqs - offset) ** 2) + (relaxation ** 2)) + noise

target = absorption(1, 500) + absorption(-1, 500)

# Cost functions
def f_phase(re, im):
    return np.var(np.arctan(re / np.abs(im)))
def f_diff(re):
    return np.linalg.norm((re / np.linalg.norm(re)) - (target / np.linalg.norm(target)))

# noise levels for the synthetic data
snrs = [5, 20, 80, 320, 1280]
# extent of phase distortions for the synthetic data, in %
phase_distortions = np.linspace(0, 1, 101)

# calculate objective function values
f_phase_objvals = np.zeros((len(snrs), len(phase_distortions)))
f_diff_objvals = np.zeros((len(snrs), len(phase_distortions)))

for i, snr in enumerate(snrs):
    for j, phase_distortion in enumerate(phase_distortions):
        # i_=in-phase, a_=antiphase, _a=absorption, _d=dispersion
        ia = absorption(1, snr) + absorption(-1, snr)
        aa = -absorption(1, snr) + absorption(-1, snr)
        id = dispersion(1, snr) + dispersion(-1, snr)
        ad = -dispersion(1, snr) + dispersion(-1, snr)
        re = ((1 - phase_distortion) * ia) + (phase_distortion * ad)
        im = (phase_distortion * aa) + ((1 - phase_distortion) * id)
        f_phase_objvals[i, j] = f_phase(re, im)
        f_diff_objvals[i, j] = f_diff(re)

# plot
fig, axs = pg.subplots2d(1, 2, figsize=(6.5, 3.5), sharey=True)
for ax, objvals, text in zip(axs, [f_phase_objvals, f_diff_objvals],
                             [r'$f_\mathrm{phase}$', r'$f_\mathrm{diff}$']):
    for i, _, color in apt.enzip(snrs, apt.PAL):
        ax.plot(phase_distortions, objvals[i, :], color=color)
    ax.set(xlabel='fraction of J-modulation',
           ylabel='objective function value')
    ax.text(s=text, x=0.03, y=0.87, transform=ax.transAxes)
    ax.label_outer()
    pg.style_axes(ax, 'plot')


fig.legend([f"SNR = {snr}" for snr in snrs], ncol=5, loc="upper center")
pg.cleanup_figure()
apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
