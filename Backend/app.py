import os
import sys
import pandas as pd
import joblib

from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter

# allow importing utils
sys.path.append("../")

from utils.extract_features import extract_features
from utils.parse_transcripts import extract_participant_text
from transcription.whisper_transcribe import transcribe_audio, count_pauses

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# load ML model
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(MODEL_DIR, "model", "alzheimer_model.pkl"))

feature_columns = [
    "total_words",
    "unique_words",
    "avg_word_length",
    "lexical_diversity",
    "repetition_rate",
    "filler_count",
    "avg_sentence_length",
    "pause_count",
    "short_word_ratio",
    "punctuation_count",
    "speaking_rate"
]

def has_repetition(text):
    words = text.split()
    counts = Counter(words)

    for w in counts:
        if counts[w] > 10:
            return True

    return False

def is_garbage(text):

    words = text.split()

    if len(words) == 0:
        return True

    unique_ratio = len(set(words)) / len(words)

    # too repetitive → garbage
    if unique_ratio < 0.10:
        return True

    return False


@app.route("/analyze", methods=["POST"])
def analyze():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio = request.files["audio"]
    filepath = os.path.join(UPLOAD_FOLDER, audio.filename)
    audio.save(filepath)

    question = request.form.get("question", "")
    transcript = transcribe_audio(filepath, question_text=question)

    # remove extra whitespace
    transcript = transcript.strip().lower()

    print("Transcript:", transcript)

    # prevent empty audio
    if os.path.getsize(filepath) < 2000:
        return jsonify({
            "error": "Audio too short. Please speak for a few seconds."
        }), 400

    # detect empty or hallucinated speech
    if len(transcript) < 5:
        return jsonify({
            "error": "No speech detected. Please answer the question."
        }), 400

    invalid_phrases = ["thank you", "hello", "bye"]

    if is_garbage(transcript):
        return jsonify({
            "error": "Invalid speech detected. Please speak clearly."
        }), 400

    clean_transcript = transcript.strip().rstrip('.!,')
    if clean_transcript in invalid_phrases or (len(transcript.split()) <= 3 and any(p in clean_transcript for p in invalid_phrases)):
        return jsonify({"error": "Invalid speech detected. Please answer the question."}), 400
    
    # Calculate audio duration from WAV (to avoid PySoundFile warnings on WebM)
    import librosa
    wav_filepath = filepath.replace(".webm", ".wav")
    try:
        if os.path.exists(wav_filepath):
            duration = float(librosa.get_duration(path=wav_filepath))
        else:
            duration = float(librosa.get_duration(path=filepath))
    except Exception as e:
        print("Duration extraction error:", e)
        duration = 0.0

    # Count physical pauses in audio
    pause_count = count_pauses(wav_filepath) if os.path.exists(wav_filepath) else 0

    features = extract_features(transcript, duration=duration, pause_count=pause_count)

    df = pd.DataFrame([features], columns=feature_columns)

    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]

    confidence = float(max(probabilities) * 100)

    label = "No Risk" if prediction == 0 else "Alzheimer Risk"

    return jsonify({
        "transcript": transcript,
        "prediction": label,
        "confidence": confidence,
        "duration": duration,
        "features" : dict(zip(feature_columns, features))
    })

@app.route("/final_predict", methods=["POST"])
def final_predict():

    data = request.get_json()
    transcript = data["transcript"]
    duration = float(data.get("duration", 0.0))
    pause_count = int(data.get("pause_count", 0))

    features = extract_features(transcript, duration=duration, pause_count=pause_count)

    df = pd.DataFrame([features], columns=feature_columns)

    prediction = model.predict(df)[0]
    prob = model.predict_proba(df)[0]

    confidence = float(max(prob) * 100)

    if confidence < 65:
        label = "Uncertain"
    else:
        label = "No Risk" if prob[0] > prob[1] else "Alzheimer Risk"

    return jsonify({
        "prediction": label,
        "confidence": confidence,
        "features": dict(zip(feature_columns, features))
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)