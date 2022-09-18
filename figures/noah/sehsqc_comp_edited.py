import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / "201115-7a-c13-sehsqc-full"
# No editing in any of these datasets
standalone = pg.read(p, [5, 4])
sc = pg.read(p, [12001, 12002])
sporc = pg.read(p, [20001, 20002])
spv1c = pg.read(p, [22001, 22002])
spv2c = pg.read(p, [24001, 24002])

texts = ['CRK', 'seHSQC1', 'seHSQC2']

fig, axs = pg.subplots(1, 3, figsize=(6.5, 3))

for dss, ax, t in zip([sporc, spv1c, spv2c], axs.flat, texts):
    apt.hsqc_cosy_stripplot(molecule=apt.Andrographolide,
                            datasets=dss, ref_datasets=sc,
                            edited=True,
                            ylabel="relative intensity",
                            xlabel='',
                            palette=apt.PAL,
                            show_categories=True,
                            ax=ax, legend=False)
    ax.label_outer()
    ax.set(ylim=(-0.45, 2.1), xlim=(-0.45, 0.45))
    ax.text(s=t, x=0.14, y=0.98, ha='left', va='top',
            transform=ax.transAxes)

apt.tl()
apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
