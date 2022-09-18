import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / "201115-7a-c13-sehsqc-full"
# No editing in any of these datasets
standalone = pg.read(p, [5, 4])
sc_noed = pg.read(p, [11001, 11002])
sc_ed = pg.read(p, [12001, 12002])

zip_noed = pg.read(p, [23001, 23002])
zip_ed = pg.read(p, [24001, 24002])
bb_noed = pg.read(p, [29001, 29002])
bb_ed = pg.read(p, [30001, 30002])

texts = ['BIG-BIRD', 'ZIP', 'BIG-BIRD edited', 'ZIP edited']

fig, axs = pg.subplots(2, 2, figsize=(5, 5.5))

for i, dss, ax, t in apt.enzip([bb_noed, zip_noed, bb_ed, zip_ed], axs.flat, texts):
    apt.hsqc_cosy_stripplot(molecule=apt.Andrographolide,
                            datasets=dss,
                            ref_datasets=(sc_ed if i >= 2 else sc_noed),
                            ylabel="relative intensity",
                            xlabel='',
                            edited=(i >= 2),
                            palette=apt.PAL,
                            show_categories=True,
                            ax=ax, legend=False)
    ax.label_outer()
    ax.set(ylim=(-0.45, 2.4), xlim=(-0.45, 0.45))
    ax.text(s=t, x=0.125, y=0.98, ha='left', va='top',
            transform=ax.transAxes)

apt.tl()
apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
