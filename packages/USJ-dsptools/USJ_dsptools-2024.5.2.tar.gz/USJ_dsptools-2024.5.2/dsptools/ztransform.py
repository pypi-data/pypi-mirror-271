"""
-----------------------------------------------------------------------------------------
ztransform module
-----------------------------------------------------------------------------------------
Provides tools for working with z-transform.
"""

from collections import namedtuple
from typing import Tuple

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def mirror_h(w: np.ndarray, h: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Mirrors a frequency response obtained with SciPy's signal.freqz() function.

    Args:
        w (np.ndarray): Frequency vector (either linear or angular frequency).

        h (np.ndarray): Transfer function.

    Returns:
        w0 (np.ndarray): Mirrored input frequency vector.

        h0 (np.ndarray): Mirrored transfer function.
    """
    Frequency_Response = namedtuple("Frequency_Response", "wo ho")

    w0 = np.r_[np.flip(-w[w > 0]), w]
    h0 = np.r_[np.flip(h[w > 0]), h]

    return Frequency_Response(w0, h0)


def z_plane(
    b: np.ndarray, a: np.ndarray, filename: str = None
) -> Tuple[np.ndarray, np.ndarray, float]:
    """Plot the complex z-plane given a transfer function coefficients in the
    form:
                Y(z)     b[0] + b[1]z^-1 + b[2]z^-2 + ... + b[N]z^-N
        H(z) = ------ = ---------------------------------------------
                X(z)     a[0] + a[1]z^-1 + a[2]z^-2 + ... + a[M]z^-M

    Args:
        b (np.ndarray): Forward (direct) coefficients.

        a (np.ndarray): Backward (recursive) coefficients. Note that the
        first coefficient should be always present.

        filename (str, optional): Name and extension of the output file to
        save the figure. Defaults to None (does not save the figure).

    Returns:
        z (np.ndarray): Values of the zeroes.

        p (np.ndarray): Values of the poles.

        k (float): Normalization coefficient.

    --------------------------------------------------------------------------------------------
    Copyright (c) 2011 Christopher Felton

    The original function was modified by Alejandro Alcaine (lalcaine@usj.es)
    in order to work with the necessary details required for the subject.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    The following is derived from the slides presented by
    Alexander Kain for CS506/606 "Special Topics: Speech Signal Processing"
    CSLU / OHSU, Spring Term 2011.
    """

    Z_Plane = namedtuple("Z_Plane", "z p k")

    # get a figure/plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca()

    # create the unit circle
    uc = mpl.patches.Circle((0, 0), radius=1, fill=False, color="black", ls="dashed")
    ax.add_patch(uc)

    # The coefficients are less than 1, normalize the coeficients
    if any(b > 1):
        kn = np.max(b)
        b = b / float(kn)
    else:
        kn = 1

    if any(a > 1):
        kd = np.max(a)
        a = a / float(kd)
    else:
        kd = 1

    degree_b = len(b) - 1
    degree_a = len(a) - 1

    if degree_b < degree_a:
        l = degree_a - degree_b
        if not b[:degree_b].any():
            b = b[-1]
            B = np.polynomial.Polynomial(b) * np.polynomial.Polynomial([0, 1]) ** l
        else:
            B = (
                np.polynomial.Polynomial(b[::-1])
                * np.polynomial.Polynomial([0, 1]) ** l
            )
        A = np.polynomial.Polynomial(a[::-1])
    elif degree_b > degree_a:
        l = degree_b - degree_a
        B = np.polynomial.Polynomial(b[::-1])
        A = np.polynomial.Polynomial(a[::-1]) * np.polynomial.Polynomial([0, 1]) ** l
    else:
        if not b[:degree_b].any():
            b = b[-1]
            B = np.polynomial.Polynomial(b)
        else:
            B = np.polynomial.Polynomial(b[::-1])
        A = np.polynomial.Polynomial(a[::-1])

    # Get the poles and zeros
    p = A.roots()
    z = B.roots()

    k = kn / float(kd)

    # Plot the zeros and set marker properties
    zu, cu = np.unique(z, return_counts=True)
    for count, zero in zip(cu , zu):
        if count > 1:
            t1 = plt.plot(zero.real, zero.imag, c="#1f77b4", marker="o", ms=10)
            plt.setp(t1, markersize=10.0, markeredgewidth=2.0, markerfacecolor="None")
            ax.annotate(
                text=str(count),
                xy=(zero.real + 0.025, zero.imag + 0.025),
                color="#1f77b4",
                fontsize="large",
                weight="bold",
            )
        else:
            t1 = plt.plot(zero.real, zero.imag, c="#1f77b4", marker="o", ms=10)
            plt.setp(t1, markersize=10.0, markeredgewidth=2.0, markerfacecolor="None")

    if p.size < z.size:
        l = z.size - p.size
        p = np.concatenate((p, np.zeros(l)))
        pu, cu = np.unique(p, return_counts=True)
        for count, pole in zip(cu, pu):
            if count > 1:
                t2 = plt.plot(pole.real, pole.imag, c="#1f77b4", marker="x", ms=10)
                plt.setp(
                    t2, markersize=12.0, markeredgewidth=2.0, markerfacecolor="None"
                )
                ax.annotate(
                    text=str(count),
                    xy=(pole.real + 0.025, pole.imag + 0.025),
                    color="#1f77b4",
                    fontsize="large",
                    weight="bold",
                )
            else:
                t2 = plt.plot(pole.real, pole.imag, c="#1f77b4", marker="x", ms=10)
                plt.setp(
                    t2, markersize=12.0, markeredgewidth=2.0, markerfacecolor="None"
                )

    else:
        pu, cu = np.unique(p, return_counts=True)
        for count, pole in zip(cu, pu):
            if count > 1:
                t2 = plt.plot(pole.real, pole.imag, c="#1f77b4", marker="x", ms=10)
                plt.setp(
                    t2, markersize=12.0, markeredgewidth=2.0, markerfacecolor="None"
                )
                ax.annotate(
                    text=str(count),
                    xy=(pole.real + 0.025, pole.imag + 0.025),
                    color="#1f77b4",
                    fontsize="large",
                    weight="bold",
                )
            else:
                t2 = plt.plot(pole.real, pole.imag, c="#1f77b4", marker="x", ms=10)
                plt.setp(
                    t2, markersize=12.0, markeredgewidth=2.0, markerfacecolor="None"
                )

    ax.spines["left"].set_position("center")
    ax.spines["bottom"].set_position("center")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    # set the ticks
    r = 1.25
    if any(p) and any(z):
        r = max(r, 1.1 * max(abs(p)), 1.1 * max(abs(z)))
    else:
        if any(p):
            r = max(r, 1.1 * max(abs(p)))
        if any(z):
            r = max(r, 1.1 * max(abs(z)))

    plt.axis("scaled")
    plt.axis([-r, r, -r, r])

    ticks = [-1, -0.5, 0.5, 1]
    plt.xticks(ticks)
    plt.yticks(ticks)

    ax.tick_params(axis="both", labelsize="x-large")  # Increase size of tick labels

    if not isinstance(filename, type(None)):
        if "." in filename:
            extension = filename[filename.find(".") + 1 :]
            filename = filename[: filename.find(".")]
        else:
            extension = "png"

        fig.savefig(
            f"{filename}.{extension}", dpi=300, format=extension, bbox_inches="tight"
        )

    plt.show()

    return Z_Plane(z, p, k)
