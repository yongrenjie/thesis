import penguins as pg
import aptenodytes as apt

apt.thesis()
path = apt.nmrd() / '211226-7a-hmbc-grad'

fig, ax = pg.subplots(figsize=(6.5, 3))
expnos = [i * 1000 + 1 for i in range(11, 17)]
dss = [pg.read(path, expno) for expno in expnos]
labels = ["Symm.",
          "Asymm. A\n$\\alpha=1.67$",
          "Asymm. A\n$\\alpha=0.6$",
          "Asymm. A\n$\\alpha=0.3$",
          "Asymm. B",
          "Asymm. C",
          ]
apt.generic_stripplot(experiment=apt.Andrographolide.hmbc,
                      datasets=dss,
                      ref_dataset=dss[0],
                      expt_labels=labels,
                      xlabel="",
                      ylabel="relative intensity",
                      palette=apt.PAL,
                      ax=ax)
pg.style_axes(ax, 'plot')

# apt.show()
apt.save(__file__)
