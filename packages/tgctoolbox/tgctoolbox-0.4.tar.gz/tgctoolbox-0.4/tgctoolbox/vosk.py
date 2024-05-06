import json
import logging

import vosk
from vosk import KaldiRecognizer

from .logger import setup_custom_logger as TGCLoggerSetup

# Initialize logger
logger = TGCLoggerSetup("vosk", level="INFO")


def transcribe_vosk(
    audio_data,
    kaldi_recognizer: KaldiRecognizer = None,
    verbose=False,
    include_partial=False,
):
    """
    Transcribe audio data using the Vosk model.

    Args:
        audio_data: The audio data to be transcribed.
        kaldi_recognizer (KaldiRecognizer): The KaldiRecognizer instance.
        verbose (bool): Flag to set verbose logging.

    Returns:
        The transcription result as a string.

    Raises:
        ValueError: If Kaldi recognizer is not specified or audio data is invalid.
    """

    # Check if Kaldi recognizer is specified
    if kaldi_recognizer is None:
        logger.error("Kaldi recognizer is not specified.")
        raise ValueError("Kaldi recognizer is not specified.")

    # Check the validity of audio data
    if not audio_data:
        logger.error("Invalid or empty audio data received.")
        raise ValueError("Invalid or empty audio data.")

    # Set logging level
    vosk.SetLogLevel(0 if verbose else -1)

    # Start transcription variable
    transcription = ""

    try:
        # Process audio data and transcribe
        if kaldi_recognizer.AcceptWaveform(audio_data):
            result = json.loads(kaldi_recognizer.Result())
            transcription = result.get("text", "")
        elif include_partial:
            partial_result = json.loads(kaldi_recognizer.PartialResult())
            transcription = partial_result.get("partial", "")

        return transcription

    except Exception as e:
        logger.error(f"Error during transcription: {e}", exc_info=True)
        raise e
