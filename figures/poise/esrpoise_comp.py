"""
Plot data for ESRPOISE CHORUS compensation. This is Fig S5 in the paper SI.
Most code written by JB, I just cleaned it up a bit and changed the style to
match the rest of the SI.
"""

import numpy as np
import matplotlib.pyplot as plt
import deerlab as dl
import penguins as pg
import aptenodytes as apt

def spectrum(data):
    # echo data
    echo = np.real(data) + 1j * np.imag(data)
    # echo interpolation for better precision on 1st order phase correction
    echo = np.interp(np.linspace(1, len(echo), 8*len(echo)),
                     np.linspace(1, len(echo), len(echo)),
                     echo)
    # find echo centre
    imax = np.argmax(np.abs(echo))
    # chop the echo for 1st order phase correction
    echo = echo[imax:]
    # adjust intensity of first point to avoid baseline error
    echo[1] = echo[1]/2

    # spectrum
    y_spec = np.fft.fftshift(np.fft.fft(echo, n=8*len(echo)))

    # automatic 0th order phase correction
    spec_ph = y_spec
    for phi0 in np.linspace(-180, 180, 4*360+1):
        spec_phi0 = y_spec * np.exp(-1j * phi0 * np.pi/180)
        if sum(np.real(spec_phi0)) > sum(np.real(spec_ph)):
            spec_ph = spec_phi0
    y_spec = np.real(spec_ph)

    sf = 1 / (0.5e-9/8)  # 0.5ns echo resolution * 8 for interpolation
    x_spec = np.linspace(-sf / 2, sf / 2, len(y_spec))  # + 1.5*82.82e6

    return x_spec, y_spec

def min_diff_FS(x_spec, y_spec, FS):
    """
    Cost function for chorus on the fly resonator compensation
    Minimizes the difference between the spectrum and the field sweep data.
    """
    spec = y_spec/np.max(y_spec)

    # interpolate spectrum with xaxis of field sweep
    spec = np.interp(FS[:, 0], x_spec, spec)

    return np.linalg.norm(FS[:, 1] - spec)


apt.thesis()

# read FS
FS = np.loadtxt('./esrpoise_data/003_FS_inverted.txt', delimiter=' ')
# FS data treatment
FS[:, 0] = FS[:, 0] * 1e9  # GHz to Hz
FS[:, 1] = FS[:, 1] - FS[1, 1]  # baseline
FS[:, 1] = FS[:, 1]/np.max(FS[:, 1])
x0, y0 = FS[:, 0], FS[:, 1]

# nothing set up
x1, y1 = dl.deerload('./esrpoise_data/014_unopt.DTA')
x1, y1 = spectrum(y1)
cf1 = min_diff_FS(x1, y1, FS)

# after amplitude optimisation
x2, y2 = dl.deerload('./esrpoise_data/014_AOopt.DTA')
x2, y2 = spectrum(y2)
cf2 = min_diff_FS(x2, y2, FS)

# after esrpoise resonator compensation
x4, y4 = dl.deerload('./esrpoise_data/014_opt1.DTA')
x4, y4 = spectrum(y4)
cf4 = min_diff_FS(x4, y4, FS)


fig, axs = plt.subplots(1, 3, sharey=True, figsize=(6.5, 2.6))

for ax, x, y, cf in zip(axs, [x1, x2, x4], [y1, y2, y4], [cf1, cf2, cf4]):
    # plot field sweep
    ax.plot(x0 * 1e-6, y0, linestyle='--', color='#999999')
    # plot the thing being compared against it
    ax.plot(x * 1e-6, y / max(y))
    # fiddle with limits and labels
    ax.set(xlim=(-135, 135), ylim=(-0.1, 1.1),
           xlabel="offset (MHz)", ylabel="intensity (au)")
    ax.label_outer()
    # add cost function value
    ax.text(x=0.98, y=0.98, s=rf'$f_\mathrm{{diff}}$ = {cf:.2f}', ha='right', va='top',
            transform=ax.transAxes)
    pg.style_axes(ax, 'plot')


apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
