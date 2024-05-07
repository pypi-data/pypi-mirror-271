import os
import ffmpeg
import tempfile
import re


def find_optimal_breakpoints(points: list[float], n: int) -> list[float]:
    """
    Generates a list of optimal breakpoints in a list of points.

    :param points: A list of points.
    :param n: The number of desired breakpoints.
    :return: A list of breakpoints.
    :raises ValueError: If `points` is empty or `n` is less than 1.
    """

    if not points:
        raise ValueError("points must not be empty")
    if n < 1:
        raise ValueError("n must be at least 1")

    result = []
    optimal_length = points[-1] / n
    current_point = 0
    last_breakpoint = 0

    for i in points[:-1]:
        if (i - last_breakpoint) >= optimal_length:
            if optimal_length - (current_point - last_breakpoint) < (i - last_breakpoint) - optimal_length:
                result.append(current_point)
            else:
                result.append(i)
            last_breakpoint = result[-1]
        current_point = i

    return result


def save_chunk_to_temp_file(input_file: str, start: float, end: float, suffix: str) -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.close()

    in_stream = ffmpeg.input(input_file)
    (
        ffmpeg.output(in_stream, temp_file.name, ss=start, t=end - start, c="copy")
        .overwrite_output()
        .run()
    )

    return temp_file.name


def get_silence_starts(input_file: str, silence_threshold: str, silence_duration: str) -> list[float]:
    silence_starts = [0.0]

    reader = (
        ffmpeg.input(input_file)
        .filter("silencedetect", n=silence_threshold, d=silence_duration)
        .output("pipe:", format="null")
        .run_async(pipe_stderr=True)
    )

    silence_end_re = re.compile(
        r" silence_end: (?P<end>[0-9]+(\.?[0-9]*)) \| silence_duration: (?P<dur>[0-9]+(\.?[0-9]*))"
    )

    while True:
        line = reader.stderr.readline().decode("utf-8")
        if not line:
            break

        match = silence_end_re.search(line)
        if match:
            silence_end = float(match.group("end"))
            silence_dur = float(match.group("dur"))
            silence_start = silence_end - silence_dur
            silence_starts.append(silence_start)

    return silence_starts


def split_audio_into_chunks(input_file: str, max_chunks: int,
                            silence_threshold: str = "-20dB", silence_duration: float = 2.0) -> list[str]:
    """
    Splits an audio file into chunks based on periods of silence.

    :param input_file: The path of the input audio file.
    :param max_chunks: The maximum number of chunks to split the audio into.
    :param silence_threshold: The threshold for detecting silence, in dB.
    :param silence_duration: The minimum duration of silence to detect, in seconds.
    :return: A list of paths of the temporary files containing the audio chunks.
    :raises ValueError: If the input file doesn't exist or isn't a valid audio file, or if max_chunks is less than 1.
    """

    if not os.path.exists(input_file):
        raise ValueError("input_file must exist")
    if not os.path.isfile(input_file):
        raise ValueError("input_file must be a file")
    if max_chunks < 1:
        raise ValueError("max_chunks must be at least 1")

    file_extension = os.path.splitext(input_file)[1]
    metadata = ffmpeg.probe(input_file)
    duration = float(metadata["format"]["duration"])

    silence_starts = get_silence_starts(input_file, silence_threshold, str(silence_duration))
    silence_starts.append(duration)

    temp_files = []
    current_chunk_start = 0.0

    n = max_chunks
    selected_items = find_optimal_breakpoints(silence_starts, n)
    selected_items.append(duration)

    for j in range(0, len(selected_items)):
        temp_file_path = save_chunk_to_temp_file(input_file, current_chunk_start, selected_items[j], suffix=file_extension)
        temp_files.append(temp_file_path)

        current_chunk_start = selected_items[j]

    return temp_files


def transcribe_file(file_path, model, lang):
    segments, info = model.transcribe(file_path, language=lang, word_timestamps=True)
    segments = list(segments)
    return segments
