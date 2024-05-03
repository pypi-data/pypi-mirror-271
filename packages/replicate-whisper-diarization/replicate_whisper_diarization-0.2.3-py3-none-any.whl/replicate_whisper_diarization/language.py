# import os
# from functools import lru_cache

# import requests
# from mediapipe.tasks import python
# from mediapipe.tasks.python import text


# @lru_cache
# def download_model():
#     url = "https://storage.googleapis.com/mediapipe-models/language_detector/language_detector/float32/latest/language_detector.tflite"

#     response = requests.get(url)

#     os.makedirs("/tmp/cache", exist_ok=True)
#     with open("/tmp/cache/language_detector.tflite", "wb") as f:
#         f.write(response.content)


# @lru_cache
# def load_model():
#     download_model()
#     base_options = python.BaseOptions(
#         model_asset_path="/tmp/cache/language_detector.tflite"
#     )
#     options = text.LanguageDetectorOptions(base_options=base_options)
#     return text.LanguageDetector.create_from_options(options)


# def detect_language(text: str):
#     model = load_model()

#     preds = model.detect(text)

#     return {pred.language_code: f"{pred.probability:.2f}" for pred in preds.detections}
