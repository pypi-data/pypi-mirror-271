import numpy as np
import os
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import librosa


def save_to_file(filename: str, voice_data: list, samplerate: int) -> None:
    """
    Takes the filename (include directory if necessary) and the voice_data as a Queue
    including the samplerate to save the audio to wav

    :param filename:
    :param voice_data:
    :param samplerate:
    :return:
    """
    try:
        if not len(voice_data) == 0:
            data = np.concatenate(voice_data, axis=0)
            write(filename, samplerate, data)
    except Exception as e:
        raise Exception("Error saving file: {0}".format(e))


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


def plot_chroma(file_direction, s, chroma):
    """
    Plots chroma values

    :param file_direction:
    :param s:
    :param chroma:
    :return:
    """
    fig, ax = plt.subplots(nrows=2, sharex=True)
    img = librosa.display.specshow(librosa.amplitude_to_db(s, ref=np.max),
                                   y_axis='log', x_axis='time', ax=ax[0])
    fig.colorbar(img, ax=[ax[0]])
    ax[0].label_outer()
    img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
    fig.colorbar(img, ax=[ax[1]])
    plt.legend()
    plt.savefig(f'{file_direction}_chroma_features.png')


def plot_spectral_contrast(file_direction, contrast):
    """
    Plots spectral contrast

    :param file_direction:
    :param contrast:
    :return:
    """
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(contrast, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectral contrast')
    plt.tight_layout()
    plt.legend()
    plt.savefig(f'{file_direction}_spectral_features.png')


def plot_onsets(file_direction, onset_env, onsets, times):
    """
    Plot onset detection

    :param file_direction:
    :param onset_env:
    :param onsets:
    :param times:
    :return:
    """
    plt.figure(figsize=(10, 5))
    plt.plot(times, onset_env / onset_env.max(), label='Normalized Onset Strength')
    plt.vlines(times[onsets], 0, 1, color='r', alpha=0.9, linestyle='--', label='Onsets')
    plt.title('Waveform and Detected Onsets')
    plt.xlabel('Time (s)')
    plt.legend()
    plt.savefig(f'{file_direction}_onset_detection.png')
