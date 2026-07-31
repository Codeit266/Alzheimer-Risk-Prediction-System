import re
import numpy as np

def extract_features(text, duration=0, pause_count=None):

    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]

    total_words = len(words)
    unique_words = len(set(words))

    avg_word_length = np.mean([len(w) for w in words]) if words else 0

    lexical_diversity = unique_words / total_words if total_words else 0

    repetition_rate = 1 - lexical_diversity

    fillers = ["um", "uh", "like", "you know"]
    text_lower = text.lower()
    filler_count = sum(text_lower.count(f) for f in fillers)

    avg_sentence_length = total_words / len(sentences) if sentences else 0

    if pause_count is None:
        pause_count = text.count("...")

    # 🔥 NEW FEATURES
    short_word_ratio = sum(1 for w in words if len(w) <= 3) / total_words if total_words else 0
    punctuation_count = len(re.findall(r'[.,!?]', text))

    # speaking rate (words per minute)
    if duration > 0:
        speaking_rate = total_words / (duration / 60.0)
    else:
        # Dynamically estimate duration based on speech characteristics if audio duration is missing
        estimated_duration = total_words * 0.4 + pause_count * 1.8 + filler_count * 0.8
        speaking_rate = total_words / (estimated_duration / 60.0) if estimated_duration > 0 else 0

    return [
        total_words,
        unique_words,
        avg_word_length,
        lexical_diversity,
        repetition_rate,
        filler_count,
        avg_sentence_length,
        pause_count,
        short_word_ratio,
        punctuation_count,
        speaking_rate
    ]