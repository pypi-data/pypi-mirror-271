import os
import logging

import replicate

logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv(
    "DIARIZATION_MODEL_NAME",
    "collectiveai-team/speaker-diarization-3",
)
MODEL_VERSION = os.getenv(
    "DIARIZATION_MODEL_VERSION",
    "f7425066750cd06fdf95b831c08bba1530f222a2eb4145f40493f431b7483b95",
)


def segmentate(
    audio_url: str,
    num_speakers: int | None = None,
    min_speakers: int | None = None,
    max_speakers: int | None = None,
    webhook_url: str | None = None,
) -> dict:
    model = replicate.models.get(MODEL_NAME)
    version = model.versions.get(MODEL_VERSION)
    replicate_input = {
        "audio_url": audio_url,
        "num_speakers": num_speakers,
        "min_speakers": min_speakers,
        "max_speakers": max_speakers,
    }
    replicate_input = {k: v for k, v in replicate_input.items() if v is not None}

    if webhook_url:
        prediction = replicate.predictions.create(
            version=version,
            input=replicate_input,
            webhook=webhook_url,
        )

        return prediction.output

    prediction = replicate.predictions.create(version=version, input=replicate_input)
    prediction.wait()

    if prediction.status == "failed":
        logger.error("Diarization failed")

    return prediction.output
