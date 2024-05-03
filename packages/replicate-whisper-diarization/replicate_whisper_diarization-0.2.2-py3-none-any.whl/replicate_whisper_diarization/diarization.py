from datetime import datetime


def convert_to_miliseconds(time_str):
    """
    Convert a time string in the format "HH:MM:SS.sss" to milliseconds.

    Args:
        time_str (str): The time string to convert.

    Returns:
        int: The equivalent time in milliseconds.
    """
    # Convert the time string to a datetime object
    time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")

    # Calculate the total milliseconds
    milliseconds = (
        time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    ) * 1000 + time_obj.microsecond // 1000
    return milliseconds


def get_word_ts_anchor(start, end, option="start"):
    """
    Returns the timestamp anchor for a word based on the given start and end timestamps.

    Parameters:
        start (float): The start timestamp of the word.
        end (float): The end timestamp of the word.
        option (str, optional): The option to determine the timestamp anchor.
            Possible values are "start", "end", or "mid". Defaults to "start".

    Returns:
        float: The timestamp anchor based on the given option.
    """
    if option == "end":
        return end
    if option == "mid":
        return (start + end) / 2
    return start


def get_words_speaker_mapping(
    word_timestamps,
    speaker_timestamps,
    word_anchor_option="start",
):
    """
    Maps each word to its corresponding speaker based on the provided word and
        speaker timestamps.

    Args:
        word_timestamps (list): A list of dictionaries containing word timestamps
            and text.
        speaker_timestamps (list): A list of tuples containing speaker timestamps.
        word_anchor_option (str, optional): The option to determine the anchor point
            of each word. Defaults to "start".

    Returns:
        list: A list of dictionaries containing the word, start time, end time, and
            speaker for each word.
    """
    num_speaker_segments = len(speaker_timestamps)

    _, speaker_end, speaker = speaker_timestamps[0]

    word_pos, turn_idx = 0, 0
    word_speaker_mapping = []
    for word_mapping in word_timestamps:
        word_start, word_end, word = (
            int(word_mapping["timestamp"][0] * 1000),
            int(word_mapping["timestamp"][1] * 1000),
            word_mapping["text"].strip(),
        )

        word_pos = get_word_ts_anchor(word_start, word_end, word_anchor_option)
        while word_pos > float(speaker_end):
            turn_idx += 1
            turn_idx = min(turn_idx, num_speaker_segments - 1)
            _, speaker_end, speaker = speaker_timestamps[turn_idx]
            if turn_idx == num_speaker_segments - 1:
                speaker_end = get_word_ts_anchor(word_start, word_end, option="end")
        word_speaker_mapping.append(
            {
                "word": word,
                "start_time": word_start,
                "end_time": word_end,
                "speaker": speaker,
            }
        )
    return word_speaker_mapping


def get_sentences_speaker_mapping(word_speaker_mapping, speaker_timestamps):
    """
    Maps words to their respective speakers and groups them into sentences based on
        speaker changes.

    Args:
        word_speaker_mapping (list): A list of dictionaries containing word-to-speaker
            mappings.
            Each dictionary should have the following keys: "word", "speaker",
                "start_time", "end_time".
        speaker_timestamps (list): A list of tuples containing speaker timestamps.
            Each tuple should have the following format: (start_time, end_time, speaker).

    Returns:
        list: A list of dictionaries representing sentences.
            Each dictionary has the following keys: "speaker", "start_time", "end_time",
            "text".

    Example:
        word_speaker_mapping = [
            {"word": "Hello", "speaker": "A", "start_time": 0.0, "end_time": 1.0},
            {"word": "world", "speaker": "A", "start_time": 1.0, "end_time": 2.0},
            {"word": "How", "speaker": "B", "start_time": 2.0, "end_time": 3.0},
            {"word": "are", "speaker": "B", "start_time": 3.0, "end_time": 4.0},
            {"word": "you", "speaker": "B", "start_time": 4.0, "end_time": 5.0},
        ]
        speaker_timestamps = [
            (0.0, 2.0, "A"),
            (2.0, 5.0, "B"),
        ]
        result = get_sentences_speaker_mapping(word_speaker_mapping, speaker_timestamps)
        print(result)
        # Output: [
        #     {"speaker": "A", "start_time": 0.0, "end_time": 2.0, "text": "Hello world "},
        #     {"speaker": "B", "start_time": 2.0, "end_time": 5.0, "text": "How are you "},
        # ]
    """
    start, end, speaker = speaker_timestamps[0]
    previous_speaker = speaker

    sentences = []
    sentence = {"speaker": speaker, "start_time": start, "end_time": end, "text": ""}

    for word_mapping in word_speaker_mapping:
        word, speaker = word_mapping["word"], word_mapping["speaker"]
        start_time, end_time = word_mapping["start_time"], word_mapping["end_time"]
        if speaker != previous_speaker:
            sentences.append(sentence)
            sentence = {
                "speaker": speaker,
                "start_time": start_time,
                "end_time": end_time,
                "text": "",
            }
        else:
            sentence["end_time"] = end_time
        sentence["text"] += word + " "
        previous_speaker = speaker

    sentences.append(sentence)
    return sentences


def remap_speaker_segments(segments: list[dict]) -> list:
    """
    Parses diarization segments and returns a list of speaker timestamps.

    Args:
        segments (list[dict]): A list of diarization segments, where each segment is a dictionary
            with keys "start", "stop", and "speaker".

    Returns:
        list: A list of speaker timestamps, where each timestamp is a list containing the start
            time (in milliseconds), stop time (in milliseconds), and speaker name.

    """
    speaker_ts = []
    for segment in segments:
        speaker_ts.append(
            [
                convert_to_miliseconds(segment["start"]),
                convert_to_miliseconds(segment["stop"]),
                segment["speaker"],
            ]
        )
    return speaker_ts


def align_word_and_speaker_segments(
    speaker_segments: list[dict],
    word_timestamps: list[dict[str, float]],
):
    """
    Aligns word and speaker segments based on the provided speaker segments and word timestamps.

    Args:
        speaker_segments (list[dict]): A list of speaker segments.
        word_timestamps (list[dict[str, float]]): A list of word timestamps.

    Returns:
        dict: A dictionary representing the alignment of word and speaker segments.
    """
    segments = remap_speaker_segments(speaker_segments)
    wsm = get_words_speaker_mapping(word_timestamps, segments, "start")
    ssm = get_sentences_speaker_mapping(wsm, segments)
    return ssm
