from pathlib import Path

import penguins as pg
import matplotlib.pyplot as plt
import numpy as np
import aptenodytes as apt

apt.thesis()

path = apt.nmrd() / "201028-7g-noah-2dj"
fig = pg.figure(figsize=(5, 4), constrained_layout=True)
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.6])
axn = fig.add_subplot(gs[0,0])
axc = fig.add_subplot(gs[0,1])
axh = fig.add_subplot(gs[1,:])
    
dss = pg.read(path, [5001, 5002, 5003])
dss[0].stage(ax=axn, levels=5e3, f1_bounds="109..132", f2_bounds="7..9.3")
dss[1].stage(ax=axc, levels=1e4, f1_bounds="15..134", f2_bounds="0.6..7.5")
dss[2].stage(ax=axh, levels=4e3, f2_bounds="0.3..9")
    
pg.mkplots([axn, axc], tight_layout=False)
pg.mkplot(axh, f1_units='Hz', tight_layout=False)
pg.ymove([axn, axc, axh], tight_layout=False)

apt.label_axes_def([axn, axc, axh])
# apt.show()
apt.save(__file__)
