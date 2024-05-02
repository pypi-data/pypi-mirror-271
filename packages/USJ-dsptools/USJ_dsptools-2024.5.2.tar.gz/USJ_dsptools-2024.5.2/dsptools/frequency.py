"""
-----------------------------------------------------------------------------------------
frequency module
-----------------------------------------------------------------------------------------
Provides frequency analysis tools.
"""

import numpy as np


def inverse_DTFS(ck: np.ndarray, t: np.ndarray, T: int, N: int) -> np.ndarray:
    """Calculates the inverse Discrete Time fourier Series.

    Args:
        ck (np.ndarray): Fourier coefficients.

        t (np.ndarray): Output time vector.

        T (int): Periodicity.

        N (int): Number of coefficients.

    Returns:
        np.ndarray: Continuous time signal.
    """

    return np.dot(
        ck, np.exp(np.outer(1j * np.arange(-N, N + 1).T * (2 * np.pi / T), t))
    )
