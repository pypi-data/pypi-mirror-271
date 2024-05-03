import os
import logging

import replicate

logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "vaibhavs10/incredibly-fast-whisper")
MODEL_VERSION = os.getenv(
    "WHISPER_MODEL_VERSION",
    "3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
)

model = replicate.models.get(MODEL_NAME)
version = model.versions.get(MODEL_VERSION)


def transcribe(
    audio_url: str,
    batch_size: int = 16,
    language: str | None = None,
    webhook_url: str | None = None,
) -> dict:
    """
    Transcribes the audio from the given URL using the Whisper diarization model.

    Args:
        audio_url (str): The URL of the audio file to transcribe.
        batch_size (int, optional): The batch size for processing the audio. Defaults to 16.
        language (str | None, optional): The language of the audio. Defaults to None.
        webhook_url (str | None, optional): The URL to send the transcription results to via webhook. Defaults to None.

    Returns:
        dict: The transcription output as a dictionary.

    Raises:
        Exception: If the transcription fails.
    """
    replicate_input = {
        "audio": audio_url,
        "batch_size": batch_size,
        "language": language,
        "timestamp": "word",
        "task": "transcribe",
    }
    replicate_input = {k: v for k, v in replicate_input.items() if v is not None}

    if webhook_url:
        prediction = replicate.predictions.create(
            version=version, input=replicate_input, webhook=webhook_url
        )

        return prediction.output

    prediction = replicate.predictions.create(version=version, input=replicate_input)
    prediction.wait()

    if prediction.status == "failed":
        logger.error("Transcription failed")

    return prediction.output
