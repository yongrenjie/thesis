import penguins as pg
import aptenodytes as apt
import matplotlib.pyplot as plt

apt.thesis()

# very descriptive naming scheme Jon
p = apt.nmrd() / 'jy 190617'

def parse_integral_file(p, expno, procno=1):
    ds = pg.read(p, expno, procno)
    art1 = ds.integrate(bounds="4.792..4.796")
    signal = ds.integrate(bounds="4.7825..4.792")
    art2 = ds.integrate(bounds="4.777..4.7825")
    return signal, signal/(0.5*(art1 + art2))

    # alternatively, can read in the data from multi_integ3
    # fpath = pg.read(p, expno, procno).path / 'integrals.txt'
    # with open(fpath) as file:
    #     for line in file:
    #         words = line.split()
    #         if len(words) == 0:
    #             continue
    #         # OK OK eval is evil but I just want to make a graph and I kinda
    #         # trust that my integrals file doesn't contain malicious code
    #         if words[0] == "1":
    #             art1 = eval(words[3])
    #         elif words[0] == "2":
    #             signal = eval(words[3])
    #         elif words[0] == "3":
    #             art2 = eval(words[3])
    # return signal, signal/(0.5*(art1 + art2))

fa_to_expno = {
    15: range(1003, 1009),
    20: range(1009, 1015),
    25: range(1015, 1021),
    28: range(1021, 1027),
    30: range(1027, 1033),
}

fig, axs = pg.subplots2d(1, 2, figsize=(6, 3), width_ratios=(1, 4))

# show the spectrum on LHS
pg.read(p, 1002).stage(ax=axs[0], bounds=(4.775, 4.80))
pg.mkplot(axs[0])

# read in reference data
double_saltire_signal, double_saltire_sar = parse_integral_file(p, 1002)

# plot the single saltire results on RHS
text_xs = [0.31, 0.48, 0.72, 1.09, 0.82]
text_ys = [1.01, 1.20, 1.12, 0.96, 0.88]
markers = ['x', 'd', 'o', '*', '+', 's']
# plot the signal/SAR on rhs
axs[1].plot([1], [1], marker='o', color='black')
axs[1].text(s='Double\nsaltire', x=1, y=1.03, ha='center')
for (fa, expno_range), color, x, y in zip(fa_to_expno.items(),
                                          pg.color_palette('bright'),
                                          text_xs, text_ys):
    signals = []
    sars = []    # ouch at variable name
    taups = []
    for expno in expno_range:
        signal, sar = parse_integral_file(p, expno)
        signals.append(signal / double_saltire_signal)
        sars.append(sar / double_saltire_sar)

        ds = pg.read(p, expno)
        rel_signal = signal / double_saltire_signal
        rel_sar = sar / double_saltire_sar
        print(f"fa={ds['cnst20']:.1f}  tp={ds['p40']/1000:.0f}ms rel_sig={rel_signal:.2f} sar={rel_sar:.2f}")
        taups.append(int(ds['p40']/1000))

    # Create markers
    for signal, sar, marker, taup in zip(signals, sars, markers, taups):
        # create dummy labels for legends which don't show up as they're
        # underneath the real ones
        if fa == 15:
            axs[1].scatter([signal], [sar], marker=marker, color='black',
                           zorder=-1, label=f"{taup} ms")
        # create the real markers
        axs[1].scatter([signal], [sar], marker=marker, color=color)

    # Create lines
    axs[1].plot(signals, sars, color=color)
    axs[1].text(s=rf'$\beta = {fa}^\circ$', x=x, y=y, ha='center',
                color=color)
    axs[1].legend(ncol=2)

apt.label_axes_def(axs)
pg.style_axes(axs[1], 'plot')
# twiddle with axes limits so that the label doesn't get in the way
xmin, xmax = axs[1].get_xlim()
axs[1].set(xlim=(xmin - 0.02, xmax), xlabel="relative signal",
           ylabel="relative signal-to-artefact ratio")
plt.subplots_adjust(wspace=0.3)
# apt.show()
apt.save(__file__)
