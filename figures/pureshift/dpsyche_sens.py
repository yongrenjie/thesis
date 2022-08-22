import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '211231-7a-dpsyche'
psyche = pg.read(p, 1003)
dpsyche_1 = pg.read(p, 1011)
dpsyche_0p8 = pg.read(p, 1012)
dpsyche_0p6 = pg.read(p, 1013)
dpsyche_0p4 = pg.read(p, 1014)
dpsyche_0p2 = pg.read(p, 1015)
dss = [dpsyche_1, dpsyche_0p8, dpsyche_0p6, dpsyche_0p4, dpsyche_0p2, psyche]

texts = [r'dPSYCHE $c = 1$', r'dPSYCHE $c = 0.8$', r'dPSYCHE $c = 0.6$',
         r'dPSYCHE $c = 0.4$', r'dPSYCHE $c = 0.2$', 'PSYCHE']

fig, axs = pg.subplots(3, 2, figsize=(6.5, 8), sharey=True)

for ax, ds, text in zip(axs.flat, dss, texts):
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
    ax.text(s=text, x=0.09, y=0.98, va='top', transform=ax.transAxes)

for ax in axs.flat:
    ax.inset1.set_ylim((min(ax.inset1.get_ylim()[0] for ax in axs.flat),
                        max(ax.inset1.get_ylim()[1] for ax in axs.flat)))
    ax.inset2.set_ylim((min(ax.inset2.get_ylim()[0] for ax in axs.flat),
                        max(ax.inset2.get_ylim()[1] for ax in axs.flat)))

apt.label_axes_def(axs)
# apt.show()
apt.save(__file__)
