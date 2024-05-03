import numpy as np
import os


def lim_y_trim(sr: float, y: np.ndarray, lim: list[float, float] = None) -> np.ndarray:
    """
    Protected method to do the checking of the limiters in all sound analysis methods
    Do not use.

    :param sr:
    :param y:
    :param lim:
    :return:
    """
    if len(lim) != 2:
        raise ValueError("lim parameter: It only accepts two items, the start_time and end_time in seconds.")

    start_index = int(lim[0] * sr)
    end_index = int(lim[1] * sr)
    y = y[start_index:end_index]

    return y


def ensure_dir_created(output_dir: str) -> None:
    """
    Util function to ensure directory has been created and if
    not then create such directory

    :param output_dir:
    :return:
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)