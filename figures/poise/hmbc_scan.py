import numpy as np
import penguins as pg
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import aptenodytes as apt

apt.thesis()

path = apt.nmrd() / "210814-7z-lpjf-scan"

cnst25s = []
cnst26s = []
cfs = []

def cf(ds):
    x = ds.proc_data()
    return np.sum(x * x)

for expno in range(101, 390):
    ds = pg.read(path, expno)
    cnst25s.append(ds['cnst25'])
    cnst26s.append(ds['cnst26'])
    cfs.append(cf(ds))

cnst25s = np.array(cnst25s)
cnst26s = np.array(cnst26s)
cfs = np.array(cfs)

min_cf = np.min(cfs)
argmin_cf = np.argmin(cfs)
print('minimum cf is ', min_cf, ' at cnst25 = ', cnst25s[argmin_cf], ' and cnst26 = ', cnst26s[argmin_cf])

cnst25s = cnst25s.reshape(17, 17)
cnst26s = cnst26s.reshape(17, 17)
cfs = cfs.reshape(17, 17)

fig, ax = plt.subplots(figsize=(5, 3))
im = ax.contourf(cnst25s, cnst26s, cfs, levels=40, cmap='viridis')
ax.set(xlabel=r"$J_\mathrm{min}$ (Hz)", ylabel=r"$J_\mathrm{max}$ (Hz)")

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)


# Optionally: show where the optimisers converge to
if 1:
    nm = [[142.032279416691, 183.80218271422535],
          [143.0683721116755, 185.70834820637296],
          [146.70082040342942, 177.69839383132492],
          [143.6949268161127, 175.10682062360974],
          [143.89969581138635, 181.36066716106518],
          ]
    mds = [[141.73333109150403, 185.82342851480672],
           [141.73333109150403, 185.82342851480672],
           [141.73333109150403, 185.82342851480672],
           [141.73333109150403, 185.82342851480672],
           [142.21861680107128, 187.63453943909872],
           ]
    bobyqa = [[135.69943209585944, 159.10230678301468],
              [136.6902693075218, 151.84489318256536],
              [153.40157753641833, 162.29689617314608],
              [135.56995896899093, 159.33347674412357],
              [133.3763611236035, 155.03334904617574],
              ]
    for alg, data, color, marker in zip(["NM", "MDS", "BOBYQA"],
                                        [nm, mds, bobyqa],
                                        apt.PAL[0:3],
                                        'xod'):
        x, y = zip(*data)
        ax.scatter(x, y, color=color, marker=marker, label=alg)
    ax.legend()


# apt.show()
apt.save(__file__)
