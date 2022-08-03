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


apt.fira()
fig, axs = plt.subplots(1, 2, figsize=(8, 3), sharey=True)

freqs = np.linspace(-20, 20, 1024)
axs[0].plot(freqs, absorption(0, 1, freqs), color='#023eff')
axs[1].plot(freqs, dispersion(0, 1, freqs), color='#023eff')

for ax in axs:
    # lifted from https://matplotlib.org/stable/gallery/spines/spine_placement_demo.html
    ax.spines.left.set_position('zero')
    ax.spines.right.set_color('none')
    ax.spines.bottom.set_position('zero')
    ax.spines.top.set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks([])

    # move '0' tick label to the left so that it doesn't sit on top of y-axis
    ax.get_xticklabels()[3].set_horizontalalignment('right')
    ax.set_xlabel(r'$\omega$ (Hz) →', loc='right')


apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
