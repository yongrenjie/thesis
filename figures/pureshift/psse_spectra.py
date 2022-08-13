"""Generates spectra to be included in psse.svg"""


import penguins as pg
import aptenodytes as apt


apt.thesis()
p = apt.nmrd() / '200816-6a-scanpsyche-fa'

zg = pg.read(p, 1)
psyche = pg.read(p, 121)

fig, axs = pg.subplots(1, 2, figsize=(5, 2.3))
b = "3.7..4.58"
zg.stage(axs[0], bounds=b)
psyche.stage(axs[1], bounds=b)

print(zg['ns'])
print(psyche['ns'])
print(zg['rg'])
print(psyche['rg'])

print(f'PSYCHE flip angle is: {psyche["cnst20"]}')

pg.mkplots(axs)

y0 = axs[0].get_ylim()
y0 = y0[1] - y0[0]
y1 = axs[1].get_ylim()
y1 = y1[1] - y1[0]
magnification = (y0 / y1) * (psyche["rg"]/zg["rg"]) * (psyche["ns"]/zg["ns"])
axs[1].text(s=f"({magnification:.1f}×)", x=4.45, y=0.1,
            transform=axs[1].get_xaxis_transform(),
            ha="right", fontsize=10)

# apt.show()
apt.save(__file__, svg=True)
