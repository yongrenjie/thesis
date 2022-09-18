import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / "201115-7a-c13-sehsqc-full"
# No editing in any of these datasets
standalone = pg.read(p, [5, 4])
sc = pg.read(p, [11001, 11002])
sporc = pg.read(p, [19001, 19002])
spv1c = pg.read(p, [21001, 21002])
spv2c = pg.read(p, [23001, 23002])

texts = ['CRK', 'seHSQC1', 'seHSQC2']

fig, axs = pg.subplots(1, 3, figsize=(6.5, 3))

for dss, ax, t in zip([sporc, spv1c, spv2c], axs.flat, texts):
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
