import matplotlib.pyplot as plt
import numpy as np
import aptenodytes as apt


def absorption(offset, k, freqs):
    """
    offset : (float) big Omega
    k      : (float) relaxation rate, 1/T2
    freqs  : (ndarray) frequency values to sample at

    All parameters should be expressed in the same units, usually Hz.
    """
    return k / ((k ** 2) + (freqs - offset) ** 2)


def dispersion(offset, k, freqs):
    """
    offset : (float) big Omega
    k      : (float) relaxation rate, 1/T2
    freqs  : (ndarray) frequency values to sample at

    All parameters should be expressed in the same units, usually Hz.
    """
    return (offset - freqs) / ((k ** 2) + (freqs - offset) ** 2)


apt.thesis()
fig, axs = plt.subplots(2, 2, figsize=(6, 5), sharey="row")

freqs = np.linspace(-30, 30, 1024)
axs[0][0].plot(freqs, -dispersion(12, 1, freqs) + dispersion(-12, 1, freqs),
               color='black', linewidth=1.2)
axs[0][1].plot(freqs, absorption(12, 1, freqs) - absorption(-12, 1, freqs),
               color='black', linewidth=1.2)
axs[1][0].plot(freqs, -dispersion(12, 1, freqs) - dispersion(-12, 1, freqs),
               color='black', linewidth=1.2)
axs[1][1].plot(freqs, absorption(12, 1, freqs) + absorption(-12, 1, freqs),
               color='black', linewidth=1.2)

for ax in axs.flat:
    ax.spines.left.set_color('none')
    ax.spines.right.set_color('none')
    ax.spines.top.set_color('none')
    ax.spines.bottom.set_position('zero')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(r'$\omega$ →', loc='right')

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
