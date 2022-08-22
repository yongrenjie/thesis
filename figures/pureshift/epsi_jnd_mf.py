import itertools
import penguins as pg
import aptenodytes as apt
import numpy as np
from numpy.fft import fft, fftshift
import matplotlib.pyplot as plt

apt.thesis()

GAMMA_H = 4258

def make_epsi_graph(ds,
                    graph_type,
                    gz_max,
                    shifts=None,
                    ax=None):
    """
    graph_type: str from {"zd", "kt", "trace"}
        Determines the type of graph drawn. See module docstring (at top of
        file) for more information.

    shifts: list of float, optional
        A list of chemical shifts for which to extract the diffusion
        attenuation curves for. Only relevant when graph_type='trace'.
        Defaults to [1.1003, 3.5687], which are respectively the CH3 and CH2
        peaks in the ethanol/D2O sample.
    """
    # --- Read in the data ---------------------------------------
    ser = ds.ser

    # --- Calculate key parameters -------------------------------
    # Number of chunks. 8 for JND data, 20 for ours
    td_psyche = ds["TD"][0]
    # Number of complex points in k-space, i.e. number of points per EPSI
    # gradient. TD2 is total number of real & imag points in FID. L3 is number
    # of EPSI loops (one loop includes both pos + neg gradient). So TD2 / (2 *
    # L3) is the number of points in one EPSI gradient (i.e. only positive
    # gradient). The extra factor of 2 is because we're interested only in
    # complex points.
    td_k = int(ds["TD"][1] / (2 * 2 * ds["L3"]))
    # Time between consecutive EPSI positive gradients, in seconds
    dw_eff = ds["AQ"][1] / ds["L3"]
    # Number of EPSI points used per PSYCHE chunk.
    # The t1 increment is in0*2, and each complex point takes dw_eff.
    npoints_per_chunk = int(ds["IN0"] * 2 / dw_eff)

    # --- Move group delay and drop points to end of FID ---------
    grpdly_points = int(ds["GRPDLY"])
    drop_points = int(ds["CNST4"])
    ser = np.roll(ser, -(grpdly_points + drop_points), axis=1)

    # --- Perform EPSI processing --------------------------------
    ser = ser.reshape((td_psyche, -1, td_k))
    # axis=0 is PSYCHE r1, axis=1 is conventional t2, axis=2 is spatial
    # dimension. Note that numpy axis order is row-major, opposite to MATLAB
    # which is column-major.

    # for i in range(td_psyche):
    #     ser[i,:,:] = np.roll(ser[i,:,:], int(-i/4))

    # Discard the part acquired with negative gradients (in principle it can be
    # added up to give sqrt(2) improvement in S/N)
    # See Frydman, JACS 2003 125 9204 for discussion.
    ser = ser[:,0::2,:]

    # --- Perform PSYCHE processing ------------------------------
    # Trim off any data beyond the chunk that is used for the final FID.
    ser = ser[:,:npoints_per_chunk,:]
    # Concatenate the chunks via reshaping.
    td_t2 = td_psyche * npoints_per_chunk
    ser = ser.reshape(td_t2, td_k)

    ## Discard any part of the spectrum that was not acquired during an EPSI
    ## gradient, i.e. if the delay D6 was nonzero.
    if ds["D6"] > 0:
        dw = ds["DW"]
        ineligible_epsi_points = int(1e6 * ds["D6"] / (dw * 2))
        td_k = td_k - ineligible_epsi_points
        ser = ser[:,:td_k]

    # --- Apodisation --------------------------------------------
    # Along k-dimension (Hamming window)
    alpha_0 = 0.54
    kls = np.linspace(0, 1, td_k)
    k_winfunc = alpha_0 - (1 - alpha_0) * np.cos(2 * np.pi * kls)
    ser = ser * k_winfunc[np.newaxis, :]
    # Along direct dimension
    t2_winfunc = np.sin(np.pi * np.linspace(0, 1, td_t2))
    ser = ser * t2_winfunc[:, np.newaxis]

    # --- Perform 2D FT ------------------------------------------
    # FT along conventional t2 dimension. This is a standard fft + fftshift.
    proc_data = fftshift(fft(ser, axis=1), axes=1)
    # FT along k-dimension. This is a conventional FT, but preceded by one
    # extra fftshift because of the pre-acquisition gradient which is half the
    # strength of one EPSI gradient. Effectively this means that k is
    # oscillating between -k_max/2 to +k_max/2, instead of between 0 and k_max
    # as is discussed in Frydman JACS 2003.
    proc_data = fftshift(fft(fftshift(proc_data, axes=0), axis=0), axes=0)

    # Calculate chemical shift range
    sw_eff = (1 / dw_eff) / ds["SFO1"][1]   # in ppm
    ppm_scale = np.linspace(ds["O1P"][1] - sw_eff/2,
                            ds["O1P"][1] + sw_eff/2,
                            td_t2)

    # Generate k-axis linspace (technically k / k_max)
    k_scale = np.linspace(-0.5, 0.5, td_k)

    # Generate t2-axis linspace
    t2_scale = np.linspace(0, dw_eff * (td_t2 - 1), td_t2)

    # Generate z-axis linspace. This equation only holds for the 600
    z_max = ds["SW_h"][1] / (GAMMA_H * gz_max * (ds["GPZ15"]/100))
    z_scale = np.linspace(-0.5, 0.5, td_k) * z_max

    # --- Plot the resulting 2D dataset --------------------------
    if graph_type == "zd":
        if ax is None:
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
        for i in range(td_k):
            # Any other type of plot (e.g. scatter()) makes it lag like crazy.
            ax.plot(xs=z_scale[i]*np.ones(td_t2),
                    ys=ppm_scale,
                    zs=np.abs(proc_data[:,i]) / np.amax(np.abs(proc_data)),  # note magnitude mode
                    linewidth=0.2, color="#023eff")
            ax.set(xlabel="z (cm)",
                   ylabel="$\\delta$ (ppm)",
                   zlabel="intensity (au)")
        for axis in [ax.w_xaxis, ax.w_yaxis, ax.w_zaxis]:
            # https://stackoverflow.com/a/57202149
            # mimic pg.style_axes(ax, 'plot')
            axis.line.set_linewidth(1.3)
    elif graph_type == "kt":
        if ax is None:
            fig, ax = plt.subplots()
        X, Y = np.meshgrid(t2_scale, k_scale)
        ax.pcolormesh(X, Y, np.abs(ser.transpose()),
                      cmap="Blues", shading="auto")
        ax.set(xlabel="$t_2$", ylabel=r"$k / k_\mathrm{max}$")
        pg.style_axes(ax, 'plot')
    elif graph_type == "trace":
        if ax is None:
            fig, ax = plt.subplots()
        if shifts is None:
            shifts = [1.1003, 3.5687]   # ethanol peaks, by default
        # Check that the requested shifts are within the SW
        if any(shift > np.max(ppm_scale) or shift < np.min(ppm_scale)
               for shift in shifts):
            raise ValueError("not all requested shifts are in spectral window")
        indices = [np.argmin(np.abs(ppm_scale - ppm)) for ppm in shifts]
        # search around those tentative indices for the tallest peaks
        margin = 5
        adjusts = [
            np.argmax(np.max(np.abs(proc_data[index-margin:index+margin, :]),
                             axis=1)) - margin
            for index in indices]
        new_indices = [i + a for i, a in zip(indices, adjusts)]
        for i in new_indices:
            ax.plot(z_scale, np.abs(proc_data[i, :]) / np.amax(np.abs(proc_data)),
                    label=f"{ppm_scale[i]:.3f} ppm")
        ax.legend()
        ax.set(xlabel=r"$z$ (cm)", ylabel="intensity (au)")
        pg.style_axes(ax, 'plot')
    return plt.gcf(), ax

path = apt.nmrd() / '1example_ufpsychedosy'
expno = 102

# rather tedious plotting process TBH
fig = pg.figure(figsize=(6.5, 8))
axs = [
    fig.add_subplot(3, 2, 1),
    fig.add_subplot(3, 2, 2),
    fig.add_subplot(3, 2, 3, projection='3d'),
    fig.add_subplot(3, 2, 4, projection='3d'),
    fig.add_subplot(3, 2, 5),
    fig.add_subplot(3, 2, 6),
]

jnd_ds = pg.read(apt.nmrd() / '1example_ufpsychedosy', 102)
mf_ds = pg.read(apt.nmrd() / '210426-6e-psycheepsi', 11)
make_epsi_graph(jnd_ds, graph_type='kt', gz_max=291, ax=axs[0])
make_epsi_graph(mf_ds, graph_type='kt', gz_max=65.7, ax=axs[1])
make_epsi_graph(jnd_ds, graph_type='zd', gz_max=291, ax=axs[2])
make_epsi_graph(mf_ds, graph_type='zd', gz_max=65.7, ax=axs[3])
make_epsi_graph(jnd_ds, graph_type='trace', gz_max=291, ax=axs[4])
make_epsi_graph(mf_ds, graph_type='trace', gz_max=65.7, ax=axs[5])

for ax in axs[2:4]:
    b = ax.get_position()
    b.x0 = b.x0 - 0.10
    ax.set_position(b)

for i, (x, y) in enumerate(itertools.product([0.117, 0.605], [0.96, 0.62, 0.308])):
    text = '(' + chr(ord('a') + i) + ')'
    fig.text(s=text, x=x, y=y, fontweight='semibold', fontsize=10)
# apt.show()
apt.save(__file__)
