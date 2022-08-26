from math import sqrt, exp, sin, cos, acos, degrees, radians
import aptenodytes as apt
import matplotlib.pyplot as plt
import penguins as pg

apt.thesis()


def ernst(tr, t1):
    """
    Calculates the Ernst angle for a given repetition time tr and T1 relaxation
    time. Returns an angle in degrees.
    """
    return degrees(acos(exp(-tr/t1)))


def signal(tr, t1, fa=None):
    """
    Calculates the amount of signal (as a fraction of the initial
    magnetisation) obtained from each FID, for a given repetition time tr and
    T1 relaxation time. The flip angle can be specified (in degrees); if it
    isn't, then the optimal Ernst angle is used (as calculated from tr and t1).
    """
    if fa is None:
        fa = ernst(tr, t1)
    c = exp(-tr / t1)
    alpha = (1 - c) / (1 - (c * cos(radians(fa))))
    return alpha * sin(radians(fa))


def experiment_snr(tr, t1, fa=None):
    """
    Calculates SNR for an experiment. This is the same as signal() except that
    the result is further divided by sqrt(tr) (because signal ~ time but noise
    ~ sqrt(time)).
    """
    return signal(tr, t1, fa) / sqrt(tr)


aqs = [1, 2, 4]
d1s = [0.01 * n for n in range(1000)]
t1 = 1.5

fig, ax = pg.subplots(figsize=(5, 3))
for aq in aqs:
    trs = [aq + d1 for d1 in d1s]
    experiment_snrs = [experiment_snr(tr, t1) for tr in trs]
    ax.plot(d1s, experiment_snrs, label=f"AQ = {aq} s",
            linewidth=aq/2)

ax.set(xlabel="D1 (s)", ylabel="sensitivity per unit time")
ax.legend()
pg.style_axes(ax, 'plot')

# apt.show()
apt.save(__file__)
