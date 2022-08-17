import penguins as pg
import aptenodytes as apt

apt.thesis()

p = apt.nmrd() / '201020-7a-timereversal'

scaled_spec = [pg.read(p, expno, 2) for expno in range(1005, 1010)]
summed_spec = pg.read(p, 2000, 1)

b = "3.80..4.87"

fig, ax = pg.subplots(figsize=(6, 5))
for spec in scaled_spec:
    spec.stage(ax, bounds=b)
summed_spec.stage(ax, bounds=b, color='black')
pg.mkplot(voffset=1.5)

for i, voffset, color in apt.enzip(ax.prop.voffsets, ax.prop.colors):
    if i < 5:
        ax.text(s=f'$j = {i + 1}$', x=4.74, y=voffset+1e5, color=color,
                transform=ax.transData, ha='center')
    else:
        ax.text(s=f'sum', x=4.74, y=voffset+1e5, color=color,
                transform=ax.transData, ha='center')

apt.show()
# apt.save(__file__)
