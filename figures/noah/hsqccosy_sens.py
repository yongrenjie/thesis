import penguins as pg
import aptenodytes as apt
from aptenodytes import Andrographolide as Andro

apt.thesis()

p = apt.nmrd() / '210723-7a-hsqc-cosy'

dsss = [
    pg.read(p, range(3001, 3004)),  # CLIP
    pg.read(p, range(4001, 4004)),  # DSE
    pg.read(p, range(5001, 5004)),  # TSE f=1
    pg.read(p, range(6001, 6004)),  # TSE f=0.8
]

ref_datasets = [
    pg.read(p, 3001),  # ScSCc HSQC-CLIP-COSY
    pg.read(p, 2001),    # SCc HSQC
    pg.read(p, 2002)     # SCc CLIP-COSY
]

texts = [
    'CLIP',
    'DSE',
    'TSE, $f = 1$',
    'TSE, $f = 0.8$'
]

fig, axs = pg.subplots(2, 2, figsize=(5, 5.5))

for i, dss, ax, t in apt.enzip(dsss, axs.flat, texts):
    apt.sscc_stripplot(molecule=Andro,
                       experiments=[Andro.hsqc_cosy, Andro.hsqc, Andro.cosy],
                       datasets=dss,
                       ref_datasets=ref_datasets,
                       ylabel="relative intensity",
                       xlabel='',
                       expt_labels=['', '', ''],
                       palette=apt.PAL,
                       ax=ax, legend=False)
    ax.label_outer()
    ax.set(ylim=(-0.45, 2.9), xlim=(-0.45, 0.45), xticks=[])
    ax.text(s=t, x=0.125, y=0.98, ha='left', va='top',
            transform=ax.transAxes)

    modules = [r'$\rm S^c$', 'S', r'$\rm C^c$']
    for j, color, m in apt.enzip(apt.PAL, modules):
        ax.text(x=-0.26+j*0.26, y=0.08, s=m,
                color=color, ha="center",
                transform=ax.get_xaxis_transform())

apt.tl()
apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
