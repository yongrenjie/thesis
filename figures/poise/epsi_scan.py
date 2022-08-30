import numpy as np
from numpy.polynomial.polynomial import Polynomial
import penguins as pg
import aptenodytes as apt

apt.thesis()
p = apt.nmrd() / 'EPSI_Scan'


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
    td_t2 = int(ds["L3"])    # int() fixes an old bug in penguins
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

def calculate_gradient_drift(path, expno, plot=None, ax=None):
    """
    Returns the amount of "gradient drift", or the drift in the maximum of the
    echo. The absolute value of this can be used as a cost function for
    optimisation.
    """
    ds = pg.read(path, expno)
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

    return cnst16, slope

cnst16s, slopes = zip(*(np.abs(calculate_gradient_drift(p, expno))
                        for expno in range(95, 117)))
fig, ax = pg.subplots(figsize=(4.5, 2.5))
ax.plot(cnst16s, slopes)

print(f'minimum at cnst16 = {cnst16s[np.argmin(slopes)]}, slope = {np.min(slopes)}')
ax.set(xlabel=r"$\alpha$", ylabel="cost function")
pg.style_axes(ax, "plot")

# apt.show()
apt.save(__file__)
