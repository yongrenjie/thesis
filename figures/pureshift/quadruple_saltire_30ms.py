import penguins as pg
import aptenodytes as apt
import numpy as np
import matplotlib.pyplot as plt

apt.thesis()
p = apt.nmrd() / "201016-7a-psyche4s-30ms"
bright = pg.color_palette('bright')
pastel = pg.color_palette('pastel')

psyche2s = [pg.read(p, expno) for expno in range(1011, 1030)]
psyche4s = [pg.read(p, expno) for expno in range(1111, 1130)]
flip_angles = [ds["cnst20"] for ds in psyche4s]


signal_bounds = (3.8415, 3.8534)  # or (4.0427, 4.0451)
art1_bounds = (3.8262, 3.8415)    # or (4.0482, 4.0576)
art2_bounds = (3.8534, 3.8704)    # or (4.0342, 4.0417)
def get_signal_and_artefact(ds):
    signal = ds.integrate(bounds=signal_bounds, mode='max')
    art1 = ds.integrate(bounds=art1_bounds, mode='max')
    art2 = ds.integrate(bounds=art2_bounds, mode='max')
    return signal, (0.5 * (art1 + art2))
def get_signal_and_sar(ds):
    signal = ds.integrate(bounds=signal_bounds, mode='max')
    art1 = ds.integrate(bounds=art1_bounds, mode='max')
    art2 = ds.integrate(bounds=art2_bounds, mode='max')
    return signal, signal / (0.5 * (art1 + art2))


fig = pg.figure(figsize=(6, 5))

subfigs = fig.subfigures(2, 1, hspace=0.1)
axs = subfigs[0].subplots(1, 2, gridspec_kw={'width_ratios': [1, 4], 'wspace': 0.3})
bottom_axs = subfigs[1].subplots(1, 2, sharey=True)

# show the peak itself in top-left
pg.read(p, 1016).stage(ax=axs[0], bounds=(3.83, 3.865))
pg.mkplot(axs[0])


# plot reference spectrum on bottom-left
bounds = (3.8, 4.95)

maybe_better_spec = psyche4s[9]
print(maybe_better_spec['cnst20'])
maybe_better_spec.stage(bottom_axs[0], bounds=bounds, color=bright[2])
bottom_axs[0].arrow(x=3.845, y=0.83, dx=0, dy=-0.1, head_width=0.02,
                    color='black', transform=bottom_axs[0].get_xaxis_transform())

ref_spec = psyche2s[2]
print(ref_spec['cnst20'])
ref_spec.stage(bottom_axs[1], bounds=bounds, color=bright[1])
bottom_axs[1].arrow(x=3.845, y=0.6, dx=0, dy=-0.1, head_width=0.02,
                    color='black', transform=bottom_axs[1].get_xaxis_transform())

pg.mkplots(bottom_axs)


# plot data on top-right
plot = 'peak_heights'

psyche2_sens = np.zeros(len(flip_angles))
psyche2_sar = np.zeros(len(flip_angles))
psyche4_sens = np.zeros(len(flip_angles))
psyche4_sar = np.zeros(len(flip_angles))

if plot == 'peak_heights':
    # similar to fa_dependence_124 plot
    # analyse data
    for i, ds2, ds4 in apt.enzip(psyche2s, psyche4s):
        sens2, sar2 = get_signal_and_artefact(ds2)
        psyche2_sens[i] = sens2; psyche2_sar[i] = sar2;
        sens4, sar4 = get_signal_and_artefact(ds4)
        psyche4_sens[i] = sens4; psyche4_sar[i] = sar4;
    axs[1].plot(flip_angles, psyche2_sens/1e5, color=bright[1], label='2 saltires')
    axs[1].plot(flip_angles, psyche2_sar/1e5, color=pastel[1], linestyle='--')
    axs[1].plot(flip_angles, psyche4_sens/1e5, color=bright[2], label='4 saltires')
    axs[1].plot(flip_angles, psyche4_sar/1e5, color=pastel[2], linestyle='--')
    axs[1].text(s="signal", x=47, y=2.00)
    axs[1].text(s="artefact", x=78, y=0.30)
    axs[1].legend(loc='best', bbox_to_anchor=(0.1, 0.7, 0.3, 0.3))

    pg.style_axes(axs[1], 'plot')
    axs[1].set(xlabel="flip angle (°)", ylabel="peak height (a.u.)")

elif plot == 'sens_and_sar':
    # similar to single_saltire plot
    # However, for this plot, it's really all over the place and not very
    # useful imo
    for i, ds2, ds4 in apt.enzip(psyche2s, psyche4s):
        sens2, sar2 = get_signal_and_sar(ds2)
        psyche2_sens[i] = sens2; psyche2_sar[i] = sar2;
        sens4, sar4 = get_signal_and_sar(ds4)
        psyche4_sens[i] = sens4; psyche4_sar[i] = sar4;
    psyche4_sens = psyche4_sens / psyche2_sens[2]
    psyche2_sens = psyche2_sens / psyche2_sens[2]
    psyche4_sar = psyche4_sar / psyche2_sar[2]
    psyche2_sar = psyche2_sar / psyche2_sar[2]
    axs[1].plot(psyche2_sens, psyche2_sar, color=bright[1], marker='x', label='2 saltires')
    axs[1].plot(psyche4_sens, psyche4_sar, color=bright[2], marker='o', label='4 saltires')
    axs[1].legend()

apt.label_axes_def([*axs, *bottom_axs])

# apt.show()
apt.save(__file__)
