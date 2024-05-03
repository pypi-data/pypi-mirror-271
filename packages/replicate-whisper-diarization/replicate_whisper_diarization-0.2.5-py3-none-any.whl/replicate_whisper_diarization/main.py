from replicate_whisper_diarization.whisper import transcribe
from replicate_whisper_diarization.segmentation import segmentate
from replicate_whisper_diarization.diarization import align_word_and_speaker_segments

# from replicate_whisper_diarization.language import detect_language
import logging

logger = logging.getLogger(__name__)


def run_transcript_with_diarization(
    audio: str,
    language: str | None = None,
    num_speakers: int | None = None,
    min_speakers: int | None = None,
    max_speakers: int | None = None,
) -> list[dict]:
    """
    Runs diarization on the given audio and returns a list of dictionaries containing word-level transcriptions
    along with speaker information.

    Args:
        audio (str): The URL of the audio file to be transcribed.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a word segment with its corresponding
        transcription and speaker information.
    """
    transcription = transcribe(audio=audio, language=language)
    speaker_segments = segmentate(audio, num_speakers, min_speakers, max_speakers)

    if not language:
        logger.error("Language not provided. using auto")
        # language = detect_language(transcription["transcript"])

    # language = transcript["detected_language"]
    word_timestamps = transcription["chunks"]
    segments = speaker_segments["segments"]
    return align_word_and_speaker_segments(segments, word_timestamps)
