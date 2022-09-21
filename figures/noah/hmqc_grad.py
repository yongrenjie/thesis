import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / '200926-7z-n15-sehsqc-full'
expnos = (101, 11, 12)   # 2 grad, 4 grad, 2 grad longer

fig, axs = pg.subplots2d(3, 3, figsize=(6.5, 6), height_ratios=[1, 0.7, 1])

# plot HMQC
for expno, ax in zip(expnos, axs[0]):
    ds = pg.read(p, expno * 1000 + 1)
    ds.stage(ax=ax, levels=3e3, f1_bounds=(86, 133), f2_bounds=(1.7, 11.2))
    pg.mkplot(ax)
    pg.ymove(ax)
# plot projections
for expno, ax in zip(expnos, axs[1]):
    proj = pg.read(p, expno * 1000 + 1).f2projp()
    proj.stage(ax=ax, bounds=(1.7, 11.2), color='black')
    pg.mkplot(ax)
# integrals
peaks = [10.70, 7.78, 2.22]
margin = 0.4
for expno, ax in zip(expnos[1:], axs[1][1:]):
    proj = pg.read(p, expno * 1000 + 1).f2projp()
    for i, peak in enumerate(peaks):
        ref_proj = pg.read(p, expnos[0] * 1000 + 1).f2projp()
        ref_integ = ref_proj.integrate(peak=peak, margin=margin, mode='max')
        integ = proj.integrate(peak=peak, margin=margin, mode='max')
        ax.text(x=peak, y=integ, transform=ax.transData,
                ha='left' if i < 2 else 'right',
                s=f'{integ/ref_integ:.2f}×', color='black')
for art in [peaks[2], 7.2]:
    axs[1][0].text(x=art, y=ref_proj.integrate(peak=art, margin=margin, mode='max'),
                   s='*', ha='center', color='red', fontsize=12)
# plot CLIP-COSY
for expno, ax in zip(expnos, axs[2]):
    ds = pg.read(p, expno * 1000 + 3)
    ds.stage(ax=ax, levels=1e5, f1_bounds=(2, 5.8), f2_bounds=(2, 4.5))
    pg.mkplot(ax)
    pg.ymove(ax)

# fix ylims for projections
ymin = min(ax.get_ylim()[0] for ax in axs[1])
ymax = max(ax.get_ylim()[1] for ax in axs[1])
for ax in axs[1]:
    ax.set_ylim((ymin, ymax * 1.2))


apt.label_axes_def(axs.T)
# apt.show()
apt.save(__file__)
