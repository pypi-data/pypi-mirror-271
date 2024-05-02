"""
-----------------------------------------------------------------------------------------
operations module
-----------------------------------------------------------------------------------------
Provides basic operations on the independent variable of signals.
"""

import numpy as np


def reflection(n: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Reflection operation.

    Args:
        n (np.ndarray): Independent variable (i.e. time vector).

        x (np.ndarray): Dependent variable (i.e. the signal).

    Returns:
        np.ndarray: Time reflected signal.
    """
    return np.r_[np.flip(x[n > 0]), x[n == 0], np.flip(x[n < 0])]


def delay(x: np.ndarray, k: int) -> np.ndarray:
    """Time delay operation.

    Args:
        x (np.ndarray): Dependent variable (i.e. the signal).

        k (int): Delay.

    Returns:
        np.ndarray: Delayed signal.
    """
    return np.roll(np.r_[np.zeros(abs(k)), x, np.zeros(abs(k))][abs(k) : -abs(k)], k)


def downsample(n: np.ndarray, x: np.ndarray, d: int) -> np.ndarray:
    """Downsample operation.

    Args:
        n (np.ndarray): Independent variable (i.e. time vector).

        x (np.ndarray): Dependent variable (i.e. the signal).

        d (int): Downsample factor.

    Returns:
        np.ndarray: Downsampled signal.
    """
    return np.pad(
        array=x[n % d == 0],
        pad_width=((len(n) - len(x[n % d == 0])) // 2,) * 2,
        mode="constant",
        constant_values=(0, 0),
    )
