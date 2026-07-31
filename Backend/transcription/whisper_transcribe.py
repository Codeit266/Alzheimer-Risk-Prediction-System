import whisper
import ffmpeg
import librosa
import numpy as np
import os
import soundfile as sf
from scipy.signal import butter, lfilter

# Load Whisper base model
model = whisper.load_model("base")


def convert_to_wav(input_path):

    output_path = input_path.replace(".webm", ".wav")

    (
        ffmpeg
        .input(input_path)
        .output(output_path, ac=1, ar=16000)
        .run(quiet=True, overwrite_output=True)
    )

    return output_path


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def preprocess_audio(wav_path):
    # Load audio at 16kHz
    y, sr = librosa.load(wav_path, sr=16000)

    # 1. Background Noise Reduction (High-pass Filter above 80Hz to remove ambient hum)
    nyq = 0.5 * sr
    low = 80.0 / nyq
    b, a = butter(4, low, btype='high')
    y_filtered = lfilter(b, a, y)

    # 2. Audio Level Normalization (Scale peak to 0.95 for clear speech levels)
    max_val = np.max(np.abs(y_filtered))
    if max_val > 0.01:
        y_norm = y_filtered * (0.95 / max_val)
    else:
        y_norm = y_filtered

    # Save preprocessed speech WAV
    sf.write(wav_path, y_norm, sr)


def is_silent(audio_path, threshold=0.005):

    y, sr = librosa.load(audio_path, sr=16000)

    if len(y) < 16000:
        return True

    energy = np.mean(np.abs(y))
    print("Energy:", energy)

    return energy < threshold


def count_pauses(wav_path, threshold_db=30, min_pause_duration_sec=0.5):
    try:
        y, sr = librosa.load(wav_path, sr=16000)
        intervals = librosa.effects.split(y, top_db=threshold_db)
        if len(intervals) <= 1:
            return 0
        
        pauses = 0
        for i in range(len(intervals) - 1):
            pause_duration = (intervals[i+1][0] - intervals[i][1]) / sr
            if pause_duration >= min_pause_duration_sec:
                pauses += 1
        return pauses
    except Exception as e:
        print("Error counting pauses:", e)
        return 0


def transcribe_audio(audio_path, question_text=""):

    # Convert to 16kHz mono WAV
    wav_path = convert_to_wav(audio_path)

    # Preprocess audio (High-pass noise filter & peak normalization)
    preprocess_audio(wav_path)

    # Check for silence
    if is_silent(wav_path):
        return ""

    # Initial prompt tuned specifically for Indian English speech verbatim transcription without hallucinated sample text
    initial_prompt = "Transcribe the exact English words spoken in Indian accent. Do not summarize or alter the spoken text."

    result = model.transcribe(
        wav_path,
        language="en",
        initial_prompt=initial_prompt,
        temperature=0.0,
        condition_on_previous_text=False,
        no_speech_threshold=0.6
    )

    return result["text"].strip()