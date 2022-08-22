import numpy as np
from numpy.fft import fft, fftshift
from numpy.polynomial.polynomial import Polynomial
import penguins as pg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import aptenodytes as apt


def process_1d_epsi(ds):
    """
    Processes an EPSI dataset (the pulse programme should be zg_epsi or
    similar) and returns three arrays:

     1. The 2D (t,k)-matrix as a numpy ndarray (axis=0 is the conventional
        t2-dimension, and axis=1 is the k-dimension).
     2. The range of t2-values as a 1D ndarray.
     3. The range of k-values as a 1D ndarray.

    This processing includes all other bells and whistles such as group delay
    removal as well as apodisation. Note that it also discards all the points
    corresponding to negative EPSI gradients.

    Parameters
    ----------
    ds : penguins.Dataset1D
        Dataset obtained via `penguins.read()`.

    Returns
    -------
    ser : numpy.ndarray
        2D numpy array. axis=0 corresponds to the t2 dimension and axis=1 to
        the k dimension.
    t2_values : numpy.ndarray
        1D array with the values of t2 at each point along the t2 axis. Useful
        for plotting.
    k_values : numpy.ndarray
        1D array with the values of k at each point along the k axis. Useful
        for plotting.
    """
    # --- Calculate key parameters -------------------------------
    fid = ds.fid
    # Number of complex points in k-space, i.e. number of points per EPSI gradient.
    # TD2 is total number of real & imag points in FID. L3 is number of EPSI loops
    # (one loop includes both pos + neg gradient). So TD2 / (2 * L3) is the number
    # of points in one EPSI gradient (i.e. only positive gradient). The extra
    # factor of 2 is because we're interested only in complex points.
    td_k = int(ds["TD"] / (2 * 2 * ds["L3"]))
    # Time between consecutive EPSI positive gradients, in seconds
    td_t2 = ds["L3"]
    dw_eff = ds["AQ"] / ds["L3"]

    # --- Move group delay and drop points to end of FID ---------
    grpdly_points = int(ds["GRPDLY"])
    fid = np.roll(fid, -grpdly_points)

    # --- Perform EPSI processing --------------------------------
    # Reshape into 2D matrix
    ser = fid.reshape((-1, td_k))
    # Discard the part acquired with negative gradients
    ser = ser[0::2,:]

    ## Discard any part of the spectrum that was not acquired during an EPSI
    ## gradient, i.e. if the delay D6 was nonzero.
    if ds["D6"] > 0:
        ineligible_epsi_points = int(1e6 * ds["D6"] / (ds["DW"] * 2))
        td_k = td_k - ineligible_epsi_points
        ser = ser[:,:td_k]

    # --- Apodisation --------------------------------------------
    # Along k-dimension (Hamming window)
    # Note that 'alpha' in MATLAB code refers to alpha_1, which is (1 - alpha_0).
    # The expression here is equivalent to MATLAB code but is closer to definition
    # given on Wikipedia.
    alpha_0 = 0.54
    ks = np.linspace(0, 1, td_k)
    k_winfunc = (alpha_0
                 - (1 - alpha_0) * np.cos(2 * np.pi * np.linspace(0, 1, td_k)))
    ser = ser * k_winfunc[np.newaxis, :]
    # Re the above line: https://numpy.org/doc/stable/user/basics.broadcasting.html
    # Along direct dimension
    t2_winfunc = np.sin(np.pi * np.linspace(0, 1, td_t2))
    ser = ser * t2_winfunc[:, np.newaxis]

    # Calculate k- and t2-axes
    t2_values = np.arange(td_t2) * dw_eff
    k_values = np.linspace(-0.5, 0.5, td_k)
    return ser, t2_values, k_values


def plot_gradient_drift(ds, graphtype=None, ax=None):
    """
    Visualise a zg_epsi dataset (or in theory, any ultrafast 2D experiment, but
    this is really designed for use with cnst16 optimisations using the zg_epsi
    pulse programme).

    Parameters
    ----------
    path : string or pathlib.Path
        Path to the NMR dataset directory (not including expno).
    expno : int
        Expno of interest.
    graphtype : string from "2d", "3d"
        Whether to plot a 2D or 3D plot.
    ax : matplotlib.axes.Axes, optional
        Axes instance to make the plot on. If 'graphtype' is '3d', this Axes must be
        created using the `projection='3d'` option. If this is not passed, a
        new Figure and Axes will be created automatically.

    Returns
    -------
    cnst16 : float
        The value of cnst16.
    slope : float
        The calculated "slope" caused by the gradient drift. Ideally this is as
        close to 0 as possible.
    fig : matplotlib.figure.Figure
    ax : matplotlib.axes.Axes
    """
    ser, t2_values, k_values = process_1d_epsi(ds)
    td_t2, td_k = ser.shape

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
    cnst16 = ds["cnst16"]
    slope = poly.coef[1]

    GAMMA_H = 4258
    gz_max = 65.7
    sw_eff = 1 / (ds["SFO1"] * (t2_values[1] - t2_values[0]))
    ppm_scale = np.linspace(ds["O1P"] - sw_eff/2, ds["O1P"] + sw_eff/2, td_t2)
    z_max = ds['SW_h'] / (GAMMA_H * gz_max * (ds["GPZ15"]/100))
    z_scale = np.linspace(-0.5, 0.5, td_k) * z_max
    proc_data = fftshift(fft(ser, axis=1), axes=1)
    proc_data = fftshift(fft(fftshift(proc_data, axes=0), axis=0), axes=0)

    fig = plt.figure(figsize=(4, 2.5))
    ax = fig.add_subplot(111, projection="3d")
    for i in range(td_k):
        # Any other type of plot (e.g. scatter()) makes it lag like crazy.
        ax.plot(xs=z_scale[i]*np.ones(td_t2),
                ys=ppm_scale,
                zs=np.abs(proc_data[:,i]) / np.amax(np.abs(proc_data)),
                linewidth=0.2, color="#023eff")
        ax.set(xlabel="z (cm)",
               ylabel="$\\delta$ (ppm)", zlabel="intensity")

apt.thesis()
p = apt.nmrd() / '210426-6e-psycheepsi'
ds = pg.read(p, 3)

plot_gradient_drift(ds=ds, graphtype='ft')
# apt.show()
apt.save(__file__, svg=True)
