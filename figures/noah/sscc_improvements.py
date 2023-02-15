import penguins as pg
import aptenodytes as apt
from aptenodytes import Andrographolide as Andro

apt.thesis()

p = apt.nmrd() / "201010-7a-hsqctocsy"
ref_s = pg.read(p, 1001)
ref_c = pg.read(p, 1002)

sscc_base  = pg.read(p, [13001, 13002, 13003])   # no mixing, SSCc, f=0.8
sspcc_base = pg.read(p, [33001, 33002, 33003])   # no mixing, SSpCc, f=0.8
sscc_dipsi = pg.read(p, [23001, 23002, 23003])   # w/ mixing, SSCc, f=0.8
mfa        = pg.read(p, [6001, 6002, 6003])      # MFA approach
dss = [sscc_base, sspcc_base, sscc_dipsi, mfa]

texts = ['S', '', r'C$\rm ^c$']

fig, axs = pg.subplots(1, 4, figsize=(6.5, 3))

for i, ds, ax in apt.enzip(dss, axs):
    apt.sscc_stripplot(
        molecule=Andro,
        datasets=ds,
        ref_datasets=[ref_s, ref_s, ref_c],
        expt_labels=['', '', ''],
        legend=False,
        xlabel='',
        ylabel='',
        palette=apt.PAL,
        ax=ax,
    )
    ax.label_outer()
    ax.set(ylim=(-0.19, 1.35), xlim=(-0.4, 0.4))

    texts[1] = r'S$^+$' if i == 1 else 'S'
    for j, color, t in apt.enzip(apt.PAL, texts):
        ax.text(x=-0.26+j*0.26, y=0.08, s=t,
                color=color, ha="center",
                transform=ax.get_xaxis_transform())
axs[0].set(ylabel="relative intensity")
for ax in axs[2:]:
    ax.text(x=0.18, y=0.978, s="+mixing", transform=ax.transAxes, va='top')

apt.tl()
apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
