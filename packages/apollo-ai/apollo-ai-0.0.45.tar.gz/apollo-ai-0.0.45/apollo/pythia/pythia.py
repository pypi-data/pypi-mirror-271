import spacy
from epitran import Epitran
from pyphen import Pyphen
import re
import jiwer
import difflib
import logging
import time
from faster_whisper import WhisperModel
import multiprocessing
import concurrent.futures
import os

from .utils import (
    transcribe_file,
    split_audio_into_chunks
)


logging.basicConfig(format='APOLLO: (%(asctime)s): %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def clean_text(text: str) -> str:
    """
    Cleans the text from all punctuation, special characters, colons and semicolons
    it only leaves tildes and double points on top of words without changing the case

    :param text:
    :return:
    """
    try:
        cleaned_text = re.sub(r'[^A-Za-z0-9áéíóúÁÉÍÓÚñÑüÜ]+', ' ', text)
        return cleaned_text
    except Exception as e:
        raise Exception("Error getting clean text: {0}".format(e))


def sentences(text: str) -> list[str]:
    """
    Extracts all the sentences in a text string conserving inner punctuation and case

    :param text:
    :return:
    """
    try:
        sentence_delimiters = r'[.!?]|(?:\.{3})|…|¡|¿|;|"'
        spanish_prefixes = ['Sr.', 'Sra.', 'Dr.', 'Lic.', 'Ing.']

        for prefix in spanish_prefixes:
            text = text.replace(prefix, prefix.replace('.', '###'))

        sentences_ = re.split(sentence_delimiters, text)

        for prefix in spanish_prefixes:
            sentences_ = [sentence.replace(prefix.replace('.', '###'), prefix) for sentence in sentences_]

        processed_sentences = []
        for sentence in sentences_:
            sentence = sentence.strip()
            if sentence and not sentence.startswith("–") and not sentence.startswith(
                    "-"):
                sentence = sentence.strip(":")
                sentence = sentence.strip(", ")
                processed_sentences.append(sentence)

        return processed_sentences

    except Exception as e:
        raise Exception('Error getting sentences: {0}'.format(e))


def word_checker(original_text: str, new_text: str) -> dict:
    """
    Compares two transcriptions and returns the correct words, incorrect
    words and omitted words

    word error rate (WER)
    match error rate (MER)
    word information lost (WIL)
    word information preserved (WIP)

    :param original_text:
    :param new_text:
    :return:
    """
    correct_words = []
    omitted_words = []

    try:
        original_words = words(original_text, True)
        new_words = words(new_text, True)

        output = jiwer.process_words(clean_text(original_text), clean_text(new_text))

        wer = output.wer
        mer = output.mer
        wip = output.wip
        wil = output.wil

        for original_word in original_words:
            if original_word in new_words:
                new_words.remove(original_word)
                correct_words.append(original_word)
            else:
                omitted_words.append(original_word)

        incorrect_words = new_words

        return {"correct_words": correct_words, "omitted_words": omitted_words, "incorrect_words": incorrect_words,
                "mer": mer, "wil": wil, "wip": wip, "wer": wer}

    except Exception as e:
        raise Exception("Error comparing words: {0}".format(e))


def word_alignment(original_text: str, new_text: str) -> dict:
    """
    Compares two transcriptions and returns word by word the difference
    marked with "*" the length of the word and the residual words in order

    Residuals are marked with "+"
    Extras are marked with "*"

    :param original_text:
    :param new_text:
    :return:
    """
    original_words = words(original_text)
    new_words = words(new_text)
    matcher = difflib.SequenceMatcher(None, original_words, new_words)
    alignment = []
    residual_words = []
    extra_words = []

    try:
        for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
            if opcode == 'equal':
                # If the words are the same, add them to the list
                alignment.extend(original_words[a0:a1])

            elif opcode == 'delete':
                # If the words are different, add asterisks to the list
                alignment.extend('+' * len(word) for word in original_words[a0:a1])
                residual_words.extend(original_words[a0:a1])

            elif opcode == 'insert' or opcode == 'replace':
                # Original transcription does not include this words
                alignment.extend('*' * len(word) for word in new_words[b0:b1])
                extra_words.extend(new_words[b0:b1])

        return {"alignment": alignment, "residual_words": residual_words, "extra_words": extra_words}
    except Exception as e:
        raise Exception("Error on word alignment: {0}".format(e))


def phonetic_transcription(text: str, lang='spa-Latn') -> str:
    """
    Cleans text and makes the phonetic following IPA

    :param text:
    :param lang:
    :return:
    """
    epi = Epitran(lang)
    try:
        return epi.transliterate(clean_text(text))
    except Exception as e:
        raise Exception("Error getting the phonetic transcription: {0}".format(e))


def syllables(text: str, lang='es') -> list[str]:
    """
    Extracts all the syllables from a text string

    :param text:
    :param lang:
    :return:
    """
    nlp = spacy.load('es_core_news_lg' if lang == 'es' else 'en_core_web_lg')
    py_instance = Pyphen(lang=lang)
    try:
        text = clean_text(text)
        doc = nlp(text)
        list_words = [token.text for token in doc]
        list_syllables = []

        for word in list_words:
            syllables_ = py_instance.inserted(word).split('-')
            list_syllables.extend(syllables_)

        return list_syllables

    except Exception as e:
        raise Exception('Error getting syllables: {0}'.format(e))


def words(text: str, lower=False, lang='es') -> list[str]:
    """
    Extracts all the words from a corpus in lower case

    :param text:
    :param lower:
    :param lang:
    :return:
    """
    nlp = spacy.load('es_core_news_lg' if lang == 'es' else 'en_core_web_lg')
    try:
        text = clean_text(text)

        if lower:
            doc = nlp(text.lower())
        else:
            doc = nlp(text)

        list_words = [token.text for token in doc]
        return list_words
    except Exception as e:
        raise Exception("Error on getting words: {0}".format(e))


def transcriber_parallel(file: str, model_name='small', device='cpu', max_processes=0, compute_type='float16',
                lang='es', silence_threshold: str = "-20dB", silence_duration: float = 2.0) -> dict:
    """
    Generates a transcription result from the given file
    it simplifies the audio loading and comes out of the box
    with all the timestamps of each word

    :param file: The name of the file
    :param model_name:
    :param device:
    :param max_processes:
    :param compute_type:
    :param lang:
    :param silence_threshold:
    :param silence_duration:
    :return:
    """
    if max_processes > multiprocessing.cpu_count() or max_processes == 0:
        max_processes = multiprocessing.cpu_count()

    temp_files_array = split_audio_into_chunks(file, max_processes, silence_threshold, silence_duration)
    model = WhisperModel(model_name, device=device, compute_type=compute_type, cpu_threads=4)
    segments_output = []
    futures = []

    try:
        logging.info("Starting transcription")
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_processes) as executor:
            for file_path in temp_files_array:
                future = executor.submit(transcribe_file, file_path, model, lang)
                futures.append(future)

        transcription = ""
        for future in futures:
            segments = future.result()

            for segment in segments:
                segments_output.append(
                    {"start": segment.start, "end": segment.end, "text": segment.text, "words": segment.words})

                transcription += segment.text + " "

        for temp_file in temp_files_array:
            os.remove(temp_file)

        return {"transcription": transcription, "segments": segments_output, "time_taken": time.time() - start_time}
    except Exception as e:
        raise Exception("Error transcribing: {0}".format(e))


def transcriber(file: str, model_name='large-v2', device='cuda', compute_type='float16', beam_size=5,
                lang='es') -> dict:
    """
    Generates a transcription result from the given file
    it simplifies the audio loading and comes out of the box
    with all the timestamps of each word

    :param file: The name of the file
    :param model_name:
    :param device:
    :param compute_type:
    :param beam_size:
    :param lang:
    :return:
    """

    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments_output = []

    try:
        logging.info("Starting transcription")
        start_time = time.time()

        segments, info = model.transcribe(file, beam_size=beam_size, language=lang, word_timestamps=True)

        transcription = ""

        for segment in segments:
            segments_output.append(
                {"start": segment.start, "end": segment.end, "text": segment.text, "words": segment.words,
                 "tokens": segment.tokens})

            transcription += segment.text + " "

        return {"transcription": transcription, "segments": segments_output, "info": info, "time_taken": time.time() - start_time}
    except Exception as e:
        raise Exception("Error transcribing: {0}".format(e))
