import matplotlib.pyplot as plt
import numpy as np
import aptenodytes as apt


def absorption(offset, k, freqs):
    """
    offset : (float) big Omega
    k      : (float) relaxation rate, 1/T2. Note that the resulting linewidth
                     is k / pi.
    freqs  : (ndarray) frequency values to sample at

    All parameters should be expressed in the same units of rad s-1
    """
    return k / ((k ** 2) + (freqs - offset) ** 2)


def dispersion(offset, k, freqs):
    """
    offset : (float) big Omega
    k      : (float) relaxation rate, 1/T2. Note that the resulting linewidth
                     is k / pi.
    freqs  : (ndarray) frequency values to sample at

    All parameters should be expressed in the same units of rad s-1
    """
    return (offset - freqs) / ((k ** 2) + (freqs - offset) ** 2)


apt.thesis()
fig, axs = plt.subplots(1, 2, figsize=(6, 2.5), sharey=True)

freqs = np.linspace(-25, 25, 1025)
axs[0].plot(freqs / (2 * np.pi), absorption(0, np.pi, freqs), color='black', linewidth=1.2)
axs[1].plot(freqs / (2 * np.pi), dispersion(0, np.pi, freqs), color='black', linewidth=1.2)

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
