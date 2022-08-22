import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '211027-6a-dpsyche'
psyche = pg.read(p, 1012)
dpsyche = pg.read(p, 1045)

fig, axs = pg.subplots(1, 2, figsize=(6.5, 3), sharey=True)

for ax, ds in zip(axs, [dpsyche, psyche]):
    ds.stage(ax, bounds="0.4..7", color='black')
    ax.inset1 = pg.mkinset(ax=ax, pos=(0.0, 0.6), size=(0.4, 0.3),
                          parent_corners=('ne', 'nw'),
                          inset_options={'edgecolor': apt.PAL[0]})
    ds.stage(ax.inset1, bounds="3.7..5.0", color=apt.PAL[0])
    ax.inset2 = pg.mkinset(ax=ax, pos=(0.42, 0.6), size=(0.4, 0.3),
                          parent_corners=('ne', 'nw'),
                          inset_options={'edgecolor': apt.PAL[1]})
    ds.stage(ax.inset2, bounds="1.55..2.65", color=apt.PAL[1])
    pg.mkplot(ax)
    pg.mkplot(ax.inset1, xlabel="")
    pg.mkplot(ax.inset2, xlabel="")

for ax in axs:
    ax.inset1.set_ylim((min(ax.inset1.get_ylim()[0] for ax in axs),
                        max(ax.inset1.get_ylim()[1] for ax in axs)))
    ax.inset2.set_ylim((min(ax.inset2.get_ylim()[0] for ax in axs),
                        max(ax.inset2.get_ylim()[1] for ax in axs)))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
