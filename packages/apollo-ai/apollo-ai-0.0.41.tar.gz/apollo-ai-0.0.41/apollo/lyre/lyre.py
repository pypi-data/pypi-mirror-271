from __future__ import annotations
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import keyboard
import librosa
import librosa.feature
import librosa.display
import matplotlib.pyplot as plt
import time
import logging
from moviepy.editor import VideoFileClip
from .utils import (
    lim_y_trim,
    ensure_dir_created,
)

logging.basicConfig(format='APOLLO: (%(asctime)s): %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def record_voice(channels: int = 1, samplerate: int = 22050, save_audio=True, output_dir='./output',
                 filename='recording',
                 timestamp: float = None) -> dict:
    """
    Records the voice in a controlled timestamp, when pressing 's'
    or stop the execution it stops the recording

    It returns a dict with the time taken and the voice data as a Queue

    Also, it calls save_audio by default to ./output

    :param filename:
    :param channels:
    :param samplerate:
    :param save_audio:
    :param output_dir:
    :param timestamp:
    :return:
    """
    if timestamp and (timestamp > 30 or timestamp < 10):
        raise ValueError("Timestamp can not be longer than 30 or smaller than 10.")

    ensure_dir_created(output_dir)

    recording = True
    buffer_length = int(samplerate * timestamp) if timestamp else None
    audio_data = np.zeros((buffer_length, channels), dtype=np.float32) if buffer_length else []

    def callback(indata, _, __, ___) -> None:
        """
        A callback function to add data to the Queue current recording

        :param indata:
        :param _:
        :param __:
        :param ___:
        :return:
        """
        if recording:
            if buffer_length:
                audio_data[:indata.shape[0]] = indata
            else:
                audio_data.append(indata.copy())

    try:
        with sd.InputStream(callback=callback, channels=channels, samplerate=samplerate):
            logging.info("Recording... Press 's' or exit to stop.")
            start_time = time.time()
            while recording:
                if timestamp and time.time() - start_time >= timestamp:
                    recording = False
                    logging.info(f"Recording Stopped after {time.time() - start_time} seconds.")
                elif keyboard.is_pressed('s'):
                    recording = False
                    logging.info("Recording Stopped")

            if save_audio:
                save_to_file("{0}/{1}.wav".format(output_dir, filename), audio_data, samplerate)

        return {"time": time.time() - start_time, "voice": audio_data, "samplerate": samplerate}
    except Exception as e:
        raise Exception("Error recording voice: {0}".format(e))


def record_ontime(channels: int, samplerate: int, save_audio=True, output_dir='./output', filename='recording',
                  timestamp: int = 30, num_recordings: int = 5) -> list:
    """
    Record audios on time to generate data every timestamp time

    :param channels:
    :param samplerate:
    :param save_audio:
    :param output_dir:
    :param filename:
    :param timestamp:
    :param num_recordings:
    :return:
    """

    audios_data = []

    try:
        for i in range(num_recordings):
            result = record_voice(channels, samplerate, save_audio, output_dir, f"{filename}_{i}", timestamp)
            audios_data.append(result)

        return audios_data
    except Exception as e:
        raise Exception("Error recording audios: {0}".format(e))


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


def convert_to_audio(video_path: str, audio_path: str):
    """
    Converts any video file (mp4 preference) to audio file (mp3 preference)
    :param video_path:
    :param audio_path:
    :return:
    """
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
    except Exception as e:
        logging.error(f"An error occurred while extracting audio: {str(e)}")
    finally:
        if 'audio_clip' in locals():
            audio_clip.close()  # Should not give an error
        if 'video_clip' in locals():
            video_clip.close()


def full_signal(filename: str, lim: list[float, float] = None, plot=False, amplitude_env=False, frame_size=1024, hop_length=512, output_dir='./output') -> dict:
    """
    Generate audio data processed with librosa to create visualizations or audio processing
    if the lim is specified then the audio is cropped to that timestamp

    :param filename:
    :param lim:
    :param plot:
    :param amplitude_env: The maximum value across the whole signal
    :param frame_size: what exactly is this?
    :param hop_length:
    :param output_dir:
    :return:
    """
    ensure_dir_created(output_dir)

    # Librosa shows its own exception
    y, sr = librosa.load(filename)
    duration = librosa.get_duration(y=y, sr=sr)

    if lim:
        y = lim_y_trim(sr, y, lim)

    amplitude_envelope = np.array([max(y[i:i+frame_size]) for i in range(0, y.size, hop_length)])

    data = {"data": y, "duration": duration, "samplerate": sr}

    if plot:
        try:
            frames = range(0, len(amplitude_envelope))
            t = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)
            plt.figure(figsize=(25, 10))
            librosa.display.waveshow(y, sr=sr)
            if amplitude_env:
                plt.plot(t, amplitude_envelope, color="r", label="Amp_env")
            plt.xlabel('Time (seconds)')
            plt.ylabel('Audio Time Series')
            plt.title('Full Signal {0}'.format(filename))
            plt.legend()
            plt.savefig(f'{output_dir}/{filename.split("/")[-1].split(".")[0]}_full_signal.png')
        except Exception as e:
            raise Exception("Error saving plot: {0}".format(e))

    if amplitude_env:
        data["amplitude_env"] = amplitude_envelope

    return data


def freq_analysis(filename: str, lim: list[float, float] = None, plot=False, n_fft=2048, hop_length=512, output_dir='./output') -> dict:
    """
    Creates a spectogram and return the data of the Fourier transform
    and the amplitude in decibels, it shows how high and how strong the frequencies are

    Good for training a machine learning model

    :param filename:
    :param lim:
    :param plot:
    :param n_fft:
    :param hop_length:
    :param output_dir:
    :return:
    """
    ensure_dir_created(output_dir)

    y, sr = librosa.load(filename)

    if lim:
        y = lim_y_trim(sr, y, lim)

    try:
        d = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        s_db = librosa.power_to_db(np.abs(d), ref=np.max)

        if plot:
            plt.figure(figsize=(25, 10))
            librosa.display.specshow(s_db, hop_length=hop_length, x_axis='time', y_axis='log')
            plt.title('Spectogram Analysis')
            plt.colorbar(format="%+2.f")
            plt.savefig(f'{output_dir}/{filename.split("/")[-1].split(".")[0]}_freq_analysis.png')

        return {"y_stft": d, "amplitude_db": s_db}
    except Exception as e:
        raise Exception("Error getting freq analysis: {0}".format(e))


def mel_freq_cepstral(filename: str, lim: list[float, float] = None, n_mfcc=13, n_fft=2048, hop_length=512, plot=False,
                      output_dir='./output') -> dict:
    """
    Audio features represent the audio's spectral features characteristics

    :param filename:
    :param lim:
    :param n_mfcc:
    :param n_fft:
    :param hop_length:
    :param plot:
    :param output_dir:
    :return:
    """
    ensure_dir_created(output_dir)

    y, sr = librosa.load(filename)

    if lim:
        y = lim_y_trim(sr, y, lim)

    try:
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)

        if plot:
            plt.figure(figsize=(25, 10))
            librosa.display.specshow(mfccs, x_axis='time')
            plt.colorbar(format="%+2.f")
            plt.legend()
            plt.savefig(f'{output_dir}/{filename.split("/")[-1].split(".")[0]}_mel_freq_cepstral.png')

        return {"mfccs": mfccs}
    except Exception as e:
        raise Exception("Error extracting audio features: {0}".format(e))


def chroma_features(filename: str, lim: list[float, float] = None, plot=False, n_chroma=12, n_fft=2048, hop_length=512,
                    output_dir='./output') -> dict:
    """
    Consisting onto 12 bins representing the 12 distinct semitones (or chroma) of the musical octave
    returns the array with the chroma of the specified time

    Computed in a larger frame with power spectogram

    :param filename:
    :param lim:
    :param plot:
    :param n_chroma:
    :param n_fft:
    :param hop_length:
    :param output_dir:
    :return:
    """
    ensure_dir_created(output_dir)

    y, sr = librosa.load(filename)

    if lim:
        y = lim_y_trim(sr, y, lim)

    try:
        s = np.abs(librosa.stft(y, n_fft=4096)) ** 2
        chroma = librosa.feature.chroma_stft(S=s, sr=sr, n_chroma=n_chroma, n_fft=n_fft, hop_length=hop_length)

        if plot:
            fig, ax = plt.subplots(nrows=2, sharex=True)
            img = librosa.display.specshow(librosa.amplitude_to_db(s, ref=np.max),
                                           y_axis='log', x_axis='time', ax=ax[0])
            fig.colorbar(img, ax=[ax[0]])
            ax[0].label_outer()
            img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
            fig.colorbar(img, ax=[ax[1]])
            plt.legend()
            plt.savefig(f'{output_dir}/{filename.split("/")[-1].split(".")[0]}_chroma_features.png')

        return {"stft_2": s, "chroma": chroma}
    except Exception as e:
        raise Exception("Error extracting chroma features: {0}".format(e))


def spectral_features(filename: str, lim: list[float, float] = None, plot=False, n_bands=6, n_fft=2048, hop_length=512,
                      output_dir='./output'):
    """
    Provides more accurate spectral contrast features compared directly from
    the audio signal

    :param filename:
    :param lim:
    :param plot:
    :param n_bands:
    :param n_fft:
    :param hop_length:
    :param output_dir:
    :return:
    """
    ensure_dir_created(output_dir)

    y, sr = librosa.load(filename)

    if lim:
        y = lim_y_trim(sr, y, lim)

    try:
        stft = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
        contrast = librosa.feature.spectral_contrast(S=stft, sr=sr, n_bands=n_bands)

        if plot:
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(contrast, x_axis='time')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Spectral contrast')
            plt.tight_layout()
            plt.legend()
            plt.savefig(f'{output_dir}/{filename.split("/")[-1].split(".")[0]}_spectral_features.png')

        return {"stft": stft, "contrast": contrast}
    except Exception as e:
        raise Exception("Error in spectral features: {0}".format(e))


def onset_detection(filename: str, lim: list[float, float] = None, plot=False, n_fft=2048, hop_length=512,
                    output_dir='./output'):
    """
    Takes audio file path and returns the detected onsets on the specified interval
    Helps identify the start oh phonemes or words

    :param filename:
    :param lim:
    :param plot:
    :param n_fft:
    :param hop_length:
    :param output_dir:
    :return:
    """
    ensure_dir_created(output_dir)

    y, sr = librosa.load(filename)

    if lim:
        y = lim_y_trim(sr, y, lim)

    try:
        stft = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
        onset_env = librosa.onset.onset_strength(S=stft, sr=sr)
        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        times = librosa.times_like(onset_env, sr=sr)

        if plot:
            plt.figure(figsize=(10, 5))
            plt.plot(times, onset_env / onset_env.max(), label='Normalized Onset Strength')
            plt.vlines(times[onsets], 0, 1, color='r', alpha=0.9, linestyle='--', label='Onsets')
            plt.title('Waveform and Detected Onsets')
            plt.xlabel('Time (seconds)')
            plt.legend()
            plt.savefig(f'{output_dir}/{filename.split("/")[-1].split(".")[0]}_onset_detection.png')

        return {"onsets": onsets, "onset_env": onset_env, "times": times[onsets]}
    except Exception as e:
        raise Exception("Error extracting onsets: {0}".format(e))
