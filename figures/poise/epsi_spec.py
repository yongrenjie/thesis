import numpy as np
from numpy.polynomial.polynomial import Polynomial
import penguins as pg
import aptenodytes as apt


apt.thesis()

p = apt.nmrd() / 'EPSI_Opt'
pscan = apt.nmrd() / 'EPSI_Scan'

def plot_kt_data(ds, ax=None):
    # EPSI processing. Look elsewhere for documentation.
    fid = ds.fid
    td_k = int(ds["TD"] / (2 * 2 * ds["L3"]))
    td_t2 = ds["L3"]
    dw_eff = ds["AQ"] / ds["L3"]
    fid = np.roll(fid, -int(ds["GRPDLY"]))
    ser = fid.reshape((-1, td_k))
    ser = ser[0::2,:]
    if ds["D6"] > 0:
        ineligible_epsi_points = int(1e6 * ds["D6"] / (ds["DW"] * 2))
        td_k = td_k - ineligible_epsi_points
        ser = ser[:,:td_k]
    alpha_0 = 0.54
    ks = np.linspace(0, 1, td_k)
    k_winfunc = (alpha_0
                 - (1 - alpha_0) * np.cos(2 * np.pi * np.linspace(0, 1, td_k)))
    ser = ser * k_winfunc[np.newaxis, :]
    t2_winfunc = np.sin(np.pi * np.linspace(0, 1, td_t2))
    ser = ser * t2_winfunc[:, np.newaxis]
    t2_values = np.arange(td_t2) * dw_eff * 1000  # note in ms
    k_values = np.linspace(-0.5, 0.5, td_k)
    abs_ser = np.abs(ser)

    # Should drop all rows (i.e. all values of t2) for which the maximum is
    # less than 20% of the overall maximum.
    threshold_amp = 0.2 * np.max(abs_ser)
    maxima_along_rows = np.max(abs_ser, axis=1)
    indices_to_use = np.nonzero(maxima_along_rows > threshold_amp)

    # Locate the maxima
    maximal_indices_along_k = np.argmax(abs_ser, axis=1)
    # Get the value of k at each maximum
    k_max_values = k_values[maximal_indices_along_k]
    poly = Polynomial.fit(x=t2_values[indices_to_use],
                          y=k_max_values[indices_to_use], deg=1)

    X, Y = np.meshgrid(t2_values, k_values)
    ax.pcolormesh(X, Y, np.abs(ser.T),
                  cmap="Blues", shading="auto")
    ax.set(xlabel=r"$t_2$ (ms)", ylabel="$k\, /\, k_\mathrm{max}$",
           ylim=(-0.15, 0.15))
    pg.style_axes(ax, "2d")
    return ds["cnst16"], poly.coef[1]

zgepsi_no_opt = pg.read(pscan, 101)
zgepsi_opt = pg.read(pscan, 105)
tocsy_no_opt = pg.read(p, 10)
tocsy_opt = pg.read(p, 11)

fig, axs = pg.subplots2d(2, 2, figsize=(6, 4.5), height_ratios=[1.2, 2])

# Plot 1Ds
_, slope_no_opt = plot_kt_data(zgepsi_no_opt, axs[0][0])
axs[0][0].text(x=0.02, y=0.02, s=(f"$\\alpha = {zgepsi_no_opt['cnst16']:.4f}$"
                                  f"\nslope = {abs(slope_no_opt):.4f}"),
               horizontalalignment="left", verticalalignment="bottom",
               transform=axs[0][0].transAxes, fontsize=10)
_, slope_opt = plot_kt_data(zgepsi_opt, axs[0][1])
axs[0][1].text(x=0.02, y=0.02, s=(f"$\\alpha = {zgepsi_opt['cnst16']:.4f}$"
                                  f"\nslope = {abs(slope_opt):.4f}"),
               horizontalalignment="left", verticalalignment="bottom",
               transform=axs[0][1].transAxes, fontsize=10)

# Plot 2Ds
f1b = (6.2, 7.65)
f2b = (6.2, 7.8)
tocsy_no_opt.stage(axs[1][0], levels=65, f1_bounds=f1b, f2_bounds=f2b)
tocsy_opt.stage(axs[1][1], levels=65, f1_bounds=f1b, f2_bounds=f2b)
pg.mkplots(axs[1])
pg.ymove(axs[1])


pg.label_axes(axs[0], fstr="({})", start=1, fontweight="semibold", offset=(0.02, 0.04))
pg.label_axes(axs[1], fstr="({})", start=3, fontweight="semibold")
# apt.show()
apt.save(__file__)
