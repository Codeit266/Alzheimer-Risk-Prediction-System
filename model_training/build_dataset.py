import os
import pandas as pd
import sys

sys.path.append("../")


from utils.parse_transcripts import extract_participant_text
from utils.extract_features import extract_features

data = []

DATA_FOLDER = "../data"

labels = {
    "control": 0,
    "dementia": 1
}

for group, label in labels.items():

    group_path = os.path.join(DATA_FOLDER, group)

    for root, dirs, files in os.walk(group_path):

        for file in files:

            if file.endswith(".cha"):

                file_path = os.path.join(root, file)

                text = extract_participant_text(file_path)

                features = extract_features(text)

                data.append(features + [label])

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

os.makedirs("features", exist_ok=True)

df.to_csv("features/dataset.csv", index=False)

print("Dataset created successfully!")