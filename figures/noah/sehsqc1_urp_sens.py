import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '220110-7a-sehsqc-urp'
# No editing in any of these datasets
sc = pg.read(p, [11001, 11002])
spv1_dp = pg.read(p, [12001, 12002])
spv1_urp = pg.read(p, [14001, 14002])
spv2 = pg.read(p, [13001, 13002])

texts = ['seHSQC1 double 90°', 'seHSQC1 URP', 'seHSQC2']

fig, axs = pg.subplots(1, 3, figsize=(6.5, 3))

for dss, ax, t in zip([spv1_dp, spv1_urp, spv2], axs.flat, texts):
    apt.hsqc_cosy_stripplot(molecule=apt.Andrographolide,
                            datasets=dss, ref_datasets=sc,
                            ylabel="relative intensity",
                            xlabel='',
                            palette=apt.PAL,
                            show_categories=True,
                            ax=ax, legend=False)
    ax.label_outer()
    ax.set(ylim=(-0.45, 2.4), xlim=(-0.45, 0.45))
    ax.text(s=t, x=0.14, y=0.98, ha='left', va='top',
            transform=ax.transAxes)

apt.tl()
apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
