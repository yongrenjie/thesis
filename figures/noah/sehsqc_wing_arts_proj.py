import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / '201115-7a-sehsqc-grads'

fig, ax = pg.subplots(figsize=(5, 3))
for expno in (1, 6, 5, 7, 8):
    ds = pg.read(p, expno * 1000 + 2)
    ds.slice(f2=0.668).stage(ax=ax, bounds=(-0.9, 2.3), color='black')
pg.mkplot(ax, voffset=0.1)

ymin, ymax = ax.get_ylim()
ax.set_ylim((ymin, ymax * 0.4))

descriptors = [
    "gradients before and after $t_1$",
    "gradient after $t_1$ only",
    "gradient before $t_1$ only",
    "no gradients",
    "gradient after $t_1$ only, 0.25× SW",
]

for i, voffset, s in apt.enzip(ax.prop.voffsets, descriptors, start=1):
    apt.label_axes_def([ax], x=0, y=voffset+800000, start=i, ha='left',
                       transform=ax.get_yaxis_transform())
    ax.text(x=0.05, y=voffset+(7e5 if i != 5 else 2e6),
            transform=ax.get_yaxis_transform(),
            s=s, ha="left", fontsize=9)

# apt.show()
apt.save(__file__)
