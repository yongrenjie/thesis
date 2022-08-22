import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '220129-7a-dpsyche'
psyche = pg.read(p, 1004)
dpsyche = pg.read(p, 1017)

fig, axs = pg.subplots(2, 1, figsize=(6.5, 6), sharey=True)

texts = [r'TSE-dPSYCHE $c = 0.4$ (fully optimised)', 'TSE-PSYCHE']

for ax, ds, text in zip(axs, [dpsyche, psyche], texts):
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

axs[0].text(s=texts[0], x=0.055, y=0.986, va='top', transform=axs[0].transAxes)
axs[1].text(s=texts[1], x=0.055, y=0.98, va='top', transform=axs[1].transAxes)

for ax in axs:
    ax.inset1.set_ylim((min(ax.inset1.get_ylim()[0] for ax in axs),
                        max(ax.inset1.get_ylim()[1] for ax in axs)))
    ax.inset2.set_ylim((min(ax.inset2.get_ylim()[0] for ax in axs),
                        max(ax.inset2.get_ylim()[1] for ax in axs)))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
