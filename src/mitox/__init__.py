from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from palettable.mycarta import Cube1_6  # type: ignore


def plot_all_spectra(ax=None, normalise=False, log=True, xy=True):
    if ax is None:
        ax = plt.gca()
    wavelengths, hb, hbo2, melanin, lipid, water = get_all_spectra()

    if normalise:
        hb_max = max(np.nanmax(hb), np.nanmax(hbo2))
        hb /= hb_max
        hbo2 /= hb_max
        melanin /= np.nanmax(melanin)
        lipid /= np.nanmax(lipid)
        water /= np.nanmax(water)
    if not log:
        if not xy:
            ax.plot(melanin, wavelengths, label="Melanin", c=Cube1_6.mpl_colors[0])
            ax.plot(hbo2, wavelengths, label="HbO$_2$", c=Cube1_6.mpl_colors[1])
            ax.plot(hb, wavelengths, label="Hb", c=Cube1_6.mpl_colors[2])
            ax.plot(lipid, wavelengths, label="Lipid", c=Cube1_6.mpl_colors[3])
            ax.plot(water, wavelengths, label="Water", c=Cube1_6.mpl_colors[5])
        else:
            ax.plot(wavelengths, melanin, label="Melanin", c=Cube1_6.mpl_colors[0])
            ax.plot(wavelengths, hbo2, label="HbO$_2$", c=Cube1_6.mpl_colors[1])
            ax.plot(wavelengths, hb, label="Hb", c=Cube1_6.mpl_colors[2])
            ax.plot(wavelengths, lipid, label="Lipid", c=Cube1_6.mpl_colors[3])
            ax.plot(wavelengths, water, label="Water", c=Cube1_6.mpl_colors[5])
    else:
        if not xy:
            ax.semilogy(melanin, wavelengths, label="Melanin", c=Cube1_6.mpl_colors[0])
            ax.semilogy(hbo2, wavelengths, label="HbO$_2$", c=Cube1_6.mpl_colors[1])
            ax.semilogy(hb, wavelengths, label="Hb", c=Cube1_6.mpl_colors[2])
            ax.semilogy(lipid, wavelengths, label="Lipid", c=Cube1_6.mpl_colors[3])
            ax.semilogy(water, wavelengths, label="Water", c=Cube1_6.mpl_colors[5])
        else:
            ax.semilogy(wavelengths, melanin, label="Melanin", c=Cube1_6.mpl_colors[0])
            ax.semilogy(wavelengths, hbo2, label="HbO$_2$", c=Cube1_6.mpl_colors[1])
            ax.semilogy(wavelengths, hb, label="Hb", c=Cube1_6.mpl_colors[2])
            ax.semilogy(wavelengths, lipid, label="Lipid", c=Cube1_6.mpl_colors[3])
            ax.semilogy(wavelengths, water, label="Water", c=Cube1_6.mpl_colors[5])


def get_all_spectra(wavelength_0=700, wavelength_1=1100, n_wavelengths=100):
    wavelengths = np.linspace(wavelength_0, wavelength_1, n_wavelengths)
    path = Path(__file__).parent

    df_hbo2 = pd.read_csv(path / "spectra/HbO2.csv", index_col=0)

    hbo2 = (
        np.interp(wavelengths, df_hbo2["0"], df_hbo2["1"], left=np.nan, right=np.nan)
        * 2.303
        * 150
        / 64500
    )

    df_hb = pd.read_csv(path / "spectra/Hb.csv", index_col=0)

    hb = (
        np.interp(wavelengths, df_hb["0"], df_hb["1"], left=np.nan, right=np.nan)
        * 2.303
        * 150
        / 64500
    )

    df_lipid = pd.read_csv(path / "spectra/lipid.csv", index_col=0)

    lipid = (
        np.interp(
            wavelengths, df_lipid["nm"], df_lipid["mu_a(/m)"], left=np.nan, right=np.nan
        )
        / 100
    )  # /cm

    df_water = pd.read_csv(path / "spectra/water_full.csv", index_col=0)

    water = np.interp(
        wavelengths,
        df_water["Wavelength (nm)"],
        df_water["Absorption (/cm)"],
        left=np.nan,
        right=np.nan,
    )
    melanin = 519 * (wavelengths / 500) ** (-3.5) * 0.4  # /cm

    return wavelengths, hb, hbo2, melanin, lipid, water


def setup_matplotlib(dpi: int = 300):
    """Setup Matplotlib with my preferred values.

    Args:
        dpi (int, optional): Set the default dpi for your figures. 300 may be too high for Jupyter, but is good for publication. Defaults to 300.
    """
    import matplotlib.pyplot as plt

    plt.rcParams["figure.dpi"] = dpi
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = 8
    plt.rcParams["axes.linewidth"] = 1
    plt.rcParams["figure.figsize"] = (4, 3)
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["lines.linewidth"] = 1
    plt.rcParams["savefig.bbox"] = None
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["xtick.major.width"] = 1
    plt.rcParams["xtick.minor.width"] = 1
    plt.rcParams["xtick.major.size"] = 3
    plt.rcParams["xtick.minor.size"] = 1.5
    plt.rcParams["xtick.minor.visible"] = True
    plt.rcParams["xtick.top"] = True
    plt.rcParams["ytick.direction"] = "in"
    plt.rcParams["ytick.major.width"] = 1
    plt.rcParams["ytick.minor.width"] = 1
    plt.rcParams["ytick.major.size"] = 3
    plt.rcParams["ytick.minor.size"] = 1.5
    plt.rcParams["ytick.minor.visible"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["lines.markersize"] = np.sqrt(5)
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.titlesize"] = "medium"
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["figure.labelsize"] = "medium"
    plt.rcParams["figure.labelweight"] = "bold"
    plt.rcParams["figure.titlesize"] = "medium"
    plt.rcParams["figure.titleweight"] = "bold"
    plt.rcParams["figure.constrained_layout.use"] = True
    plt.rcParams["mathtext.fontset"] = "stixsans"
    plt.rcParams["svg.fonttype"] = "none"
