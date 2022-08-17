import penguins as pg
import aptenodytes as apt
import numpy as np

apt.thesis()

t = np.linspace(0, 1, 301)
taup = 0.03
bw = 10000
s_sm = 0.2

phi = np.pi * taup * bw * ((t - 0.5) ** 2)
cx = np.cos(phi)
cy = np.sin(phi)
f_sm = np.piecewise(t, [t < s_sm, (t >= s_sm) & (t <= 1 - s_sm), t > 1 - s_sm],
                    [lambda t: np.sin(np.pi * t / (2 * s_sm)),
                     lambda t: 1,
                     lambda t: np.sin(np.pi * (1 - t) / (2 * s_sm))])

fig, axs = pg.subplots2d(2, 2, figsize=(6.5, 3), sharex=True)

b = pg.color_palette('bright')[0]
axs[0][0].plot(t * taup, phi % (2 * np.pi), linewidth=0.5, color=b)
axs[0][1].plot(t * taup, f_sm, color=b)
axs[1][0].plot(t * taup, cx, linewidth=0.5, color=b)
axs[1][1].plot(t * taup, cy, linewidth=0.5, color=b)

for ax in axs.flat:
    ax.set_xlim(-0.005, 0.035)
    pg.style_axes(ax, 'plot')
for ax in axs[1]:
    ax.set_xlabel(r'$\tau_\mathrm{p}$ (ms)')
axs[0][0].set_ylabel(r'$\phi$ (rad)')
axs[0][1].set_ylabel(r'$f_\mathrm{sm}$')
axs[1][0].set_ylabel(r'$c_x/A$')
axs[1][1].set_ylabel(r'$c_y/A$')

apt.label_axes_def(axs)
pg.tight_layout()
# apt.show()
apt.save(__file__)
