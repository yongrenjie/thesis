import penguins as pg
import aptenodytes as apt
import numpy as np

apt.thesis()
p = apt.nmrd() / 'jy-190831-chirppsychetest'


def parse_shaped_file(fname):
    amps = []
    phases = []
    with open(fname) as file:
        for line in file:
            if line.startswith("##") or line.strip() == "":
                continue
            else:
                try:
                    words = line.split()
                    amp = float(words[0])
                    phase = float(words[1])
                except:
                    continue
                else:
                    amps.append(amp)
                    phases.append(phase)
    amps = np.array(amps) / 100
    phases = np.radians(np.array(phases))
    return amps * np.cos(phases), amps * np.sin(phases)


saltire_tse = pg.read(p, 19)      # interferogram
saltire_tse_proc = pg.read(p, 20)  # processed 1D
newpulse_tse = pg.read(p, 21)    # interferogram
newpulse_tse_proc = pg.read(p, 22)  # processed 1D

fig, axs = pg.subplots2d(2, 2, height_ratios=[1, 2], figsize=(6.5, 4),
                         sharey='row')


saltire_cx, saltire_cy = parse_shaped_file(saltire_tse.path.parents[1] / 'spnam24')
newpulse_cx, newpulse_cy = parse_shaped_file(newpulse_tse.path.parents[1] / 'spnam24')
axs[0][0].plot(np.linspace(0, 1, saltire_cx.size), saltire_cx, linewidth=0.5)
axs[0][0].plot(np.linspace(0, 1, saltire_cx.size), saltire_cy, linewidth=0.5)
axs[0][1].plot(np.linspace(0, 1, newpulse_cx.size), newpulse_cx, linewidth=0.5)
axs[0][1].plot(np.linspace(0, 1, newpulse_cx.size), newpulse_cy, linewidth=0.5)
axs[0][0].set_ylabel("$c_x/A$ and $c_y/A$")
axs[0][1].set_xlabel(r"$t / \tau_\mathrm{p}$")
pg.style_axes(axs[0][0], 'plot')
pg.style_axes(axs[0][1], 'plot')
saltire_tse_proc.stage(axs[1][0], bounds=(4.72, 5.94), color='black')
newpulse_tse_proc.stage(axs[1][1], bounds=(4.72, 5.94), color='black')
pg.mkplots(axs[1])

apt.label_axes_def(axs.flat)
# apt.show()
apt.save(__file__)
