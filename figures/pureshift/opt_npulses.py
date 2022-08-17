import penguins as pg
import aptenodytes as apt

apt.thesis()


# parse data
npulses = []
fmins = []
with open('opt_npulses.out') as file:
    for line in file:
        if line.startswith("Optimising"):
            npulses.append(int(line.split()[5]))
        elif line.strip().startswith("Minimum found"):
            fmins.append(float(line.split()[-1]))

print(npulses)
print(fmins)

fig, ax = pg.subplots(figsize=(5, 3))
ax.scatter(npulses, fmins)
ax.set(xlabel="Number of pulses", ylabel="best cost function value")
pg.style_axes(ax, 'plot')
# apt.show()
apt.save(__file__)
