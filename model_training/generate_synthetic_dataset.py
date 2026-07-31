import os
import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

n_samples = 10000

data = []

# Generate controls (healthy speech pattern)
for _ in range(n_samples):
    total_words = int(np.random.normal(80, 25))
    if total_words < 15: 
        total_words = 15
    
    lexical_diversity = np.random.normal(0.72, 0.06)
    lexical_diversity = np.clip(lexical_diversity, 0.45, 0.95)
    
    unique_words = int(total_words * lexical_diversity)
    repetition_rate = 1.0 - lexical_diversity
    
    avg_word_length = np.random.normal(4.0, 0.4)
    avg_word_length = np.clip(avg_word_length, 3.0, 5.5)
    
    # Scale filler_count: Control filler rate is ~1.0%
    filler_count = np.random.poisson(total_words * 0.010)
    
    avg_sentence_length = np.random.normal(9.0, 3.0)
    avg_sentence_length = np.clip(avg_sentence_length, 4.0, 18.0)
    
    # Scale pause_count: Control pause rate is ~1.2%
    pause_count = np.random.poisson(total_words * 0.012)
    
    short_word_ratio = np.random.normal(0.44, 0.08)
    short_word_ratio = np.clip(short_word_ratio, 0.2, 0.65)
    
    punctuation_count = int(total_words / avg_sentence_length)
    if punctuation_count < 1: 
        punctuation_count = 1
    
    speaking_rate = np.random.normal(135.0, 15.0)
    speaking_rate = np.clip(speaking_rate, 90.0, 180.0)
    
    data.append([
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
        speaking_rate,
        0  # control
    ])

# Generate dementia (Alzheimer's risk speech pattern)
for _ in range(n_samples):
    total_words = int(np.random.normal(55, 15))
    if total_words < 15: 
        total_words = 15
    
    lexical_diversity = np.random.normal(0.46, 0.06)
    lexical_diversity = np.clip(lexical_diversity, 0.25, 0.65)
    
    unique_words = int(total_words * lexical_diversity)
    repetition_rate = 1.0 - lexical_diversity
    
    avg_word_length = np.random.normal(3.7, 0.3)
    avg_word_length = np.clip(avg_word_length, 2.8, 4.8)
    
    # Scale filler_count: Dementia filler rate is ~7.5%
    filler_count = np.random.poisson(total_words * 0.075)
    
    avg_sentence_length = np.random.normal(6.5, 1.5)
    avg_sentence_length = np.clip(avg_sentence_length, 3.0, 10.0)
    
    # Scale pause_count: Dementia pause rate is ~8.0%
    pause_count = np.random.poisson(total_words * 0.08)
    
    short_word_ratio = np.random.normal(0.50, 0.05)
    short_word_ratio = np.clip(short_word_ratio, 0.3, 0.7)
    
    punctuation_count = int(total_words / avg_sentence_length)
    if punctuation_count < 1: 
        punctuation_count = 1
    
    speaking_rate = np.random.normal(85.0, 18.0)
    speaking_rate = np.clip(speaking_rate, 40.0, 130.0)
    
    data.append([
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
        speaking_rate,
        1  # dementia (AD risk)
    ])

columns = [
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
    "speaking_rate",
    "label"
]

df = pd.DataFrame(data, columns=columns)

# Ensure output folder exists
os.makedirs("features", exist_ok=True)
df.to_csv("features/dataset.csv", index=False)
print("Synthetic dataset created successfully at model_training/features/dataset.csv!")
