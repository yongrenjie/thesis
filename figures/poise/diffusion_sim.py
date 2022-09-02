import numpy as np
import matplotlib.pyplot as plt
import aptenodytes as apt
import penguins as pg


apt.thesis()

fig, ax = plt.subplots(figsize=(5.5, 3))

grey = '#999999'

G = np.array([i * i for i in range(16)])

c1 = 1e-6
ax.scatter(G, np.exp(-G * G * c1), marker='x', color='black')
ax.plot(G, np.exp(-G * G * c1), color=grey, zorder=-1)
ax.text(s='(a)', x=210, y=0.9, fontweight='semibold', fontsize=10)

c2 = 5e-5
ax.scatter(G, np.exp(-G * G * c2), marker='x', color='black')
ax.plot(G, np.exp(-G * G * c2), color=grey, zorder=-1)
ax.text(s='(b)', x=132, y=0.46, fontweight='semibold', fontsize=10)

c3 = 5e-3
ax.scatter(G, np.exp(-G * G * c3), marker='x', color='black')
ax.plot(G, np.exp(-G * G * c3), color=grey, zorder=-1)
ax.text(s='(c)', x=110, y=0.04, fontweight='semibold', fontsize=10)

ax.set(ylim=(-0.05, 1.05), xlabel=r'$G$', ylabel='attenuation', xticks=[])
pg.style_axes(ax, 'plot')

# apt.show()
apt.save(__file__)
