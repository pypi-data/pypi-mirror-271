from __future__ import annotations
import sounddevice as sd
import numpy as np
import json
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
    save_to_file,
    plot_chroma,
    plot_onsets,
    plot_spectral_contrast,
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


def convert_to_audio(video_path: str, audio_path: str):
    """
    Converts any video file (mp4 preference) to audio file (mp3 preference)
    :param video_path:
    :param audio_path:
    :return:
    """
    audio_clip = None  # Initialize the variable
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
    except Exception as e:
        logging.error(f"An error occurred while extracting audio: {str(e)}")
    finally:
        if audio_clip is not None:
            audio_clip.close()  # Should not give an error
        if 'video_clip' in locals():
            video_clip.close()


def voice_intensity(filepath: str, lim: list[float, float] = None, plot=False, amplitude_env=False, frame_size=1024,
                    hop_length=512, output_dir='./output') -> str:
    """
    Generate audio data processed with librosa to create visualizations or audio processing
    if the lim is specified then the audio is cropped to that timestamp

    :param filepath: path to the audio file
    :param lim: list of two floats specifying start and end time for cropping (optional)
    :param plot: boolean flag to generate a plot (optional)
    :param amplitude_env: boolean flag to calculate the amplitude envelope (optional)
    :param frame_size: size of the STFT window (default: 1024)
    :param hop_length: hop length between consecutive STFT windows (default: 512)
    :param output_dir: directory to save the plot (default: ./output)
    :return: dictionary containing processed audio data
    """
    ensure_dir_created(output_dir)

    file_direction = output_dir + "/" + filepath.split("/")[-1].split(".")[0]

    try:
        y, sr = librosa.load(filepath)
        logging.info("Audio found, starting intensity processing...")
        duration = librosa.get_duration(y=y, sr=sr)

        if lim:
            y = librosa.util.sync(y, lim, sr=sr)

        # Calculate STFT and amplitude envelope
        stft = np.abs(librosa.stft(y, n_fft=frame_size, hop_length=hop_length))
        amplitude_envelope = np.array([max(y[i:i+frame_size]) for i in range(0, y.size, hop_length)])

        # Convert amplitude envelope to dB
        amplitude_envelope_db = librosa.amplitude_to_db(amplitude_envelope)

        max_amplitude = np.max(np.abs(y))

        data = {
            "duration": duration,
            "samplerate": sr,
            "max_amplitude": max_amplitude.tolist(),
            "stft": stft.tolist(),
            "amplitude_envelope_db": amplitude_envelope_db.tolist(),
        }

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
                plt.title('Full Signal')
                plt.legend()
                plt.savefig(f'{file_direction}_full_signal.png')
            except Exception as e:
                raise Exception("Error saving plot: {0}".format(e))

    except Exception as e:
        raise Exception(f"An error occurred while processing audio: {str(e)}")

    return json.dumps(data)


def voice_expression(filepath: str, lim: list[float, float] = None, plot=False, output_dir='./output') -> str:
    """
    Generates voice expression data

    :param filepath:
    :param lim:
    :param plot:
    :param output_dir:
    :return:
    """
    ensure_dir_created(output_dir)

    file_direction = output_dir + "/" + filepath.split("/")[-1].split(".")[0]

    try:
        y, sr = librosa.load(filepath)
        logging.info("Audio found, starting expression processing...")

        if lim:
            y = lim_y_trim(sr, y, lim)

        # Chroma features
        n_chroma = 12
        n_fft = 2048
        hop_length = 512
        s = np.abs(librosa.stft(y, n_fft=n_fft)) ** 2
        chroma = librosa.feature.chroma_stft(S=s, sr=sr, n_chroma=n_chroma, n_fft=n_fft, hop_length=hop_length)

        # Spectral features
        n_bands = 6
        stft = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
        contrast = librosa.feature.spectral_contrast(S=stft, sr=sr, n_bands=n_bands)

        # Onset detection
        onset_env = librosa.onset.onset_strength(S=stft, sr=sr)
        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        times = librosa.times_like(onset_env, sr=sr)

        # Generate plots if requested
        if plot:
            plot_chroma(file_direction, s, chroma)
            plot_spectral_contrast(file_direction, contrast)
            plot_onsets(file_direction, onset_env, onsets, times)

        data = {
            "chroma": chroma.tolist(),
            "spectral_contrast": contrast.tolist(),
            "onsets": onsets.tolist(),
            "onset_envelope": onset_env.tolist(),
            "onset_times": times[onsets].tolist(),
        }

        return json.dumps(data)

    except Exception as e:
        raise Exception(f"Error processing voice: {e}")
