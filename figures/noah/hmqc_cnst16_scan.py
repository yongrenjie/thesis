import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / '200926-7z-n15-cnst16-scan'

dss = [pg.read(p, e * 1000 + 1) for e in range(1, 17)]
projs = [ds.f2projp() for ds in dss]
cnst16s = [ds['cnst16'] for ds in dss]

peaks = [10.70, 7.78, 2.22]
margin = 0.4
peak1_ints = [proj.integrate(peaks[0], margin=margin) for proj in projs]
peak2_ints = [proj.integrate(peaks[1], margin=margin) for proj in projs]
artef_ints = [proj.integrate(peaks[2], margin=margin) for proj in projs]

fig, ax = pg.subplots(figsize=(4, 3))
ax.plot(cnst16s, peak1_ints, label='peak (10.70 ppm)')
ax.plot(cnst16s, peak2_ints, label='peak (7.78 ppm)')
ax.plot(cnst16s, artef_ints, linestyle='--', color=apt.PAL[7], label='artefact (2.22 ppm)')
ax.legend()
ax.set_xlabel('gradient duration (ms)')
ax.set_ylabel('intensity')
pg.style_axes(ax, 'plot')

# apt.show()
apt.save(__file__)
