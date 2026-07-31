from utils.parse_transcripts import parse_cha_file
from utils.extract_features import extract_features

text, duration = parse_cha_file("temp.cha")

print("Text:", text)
print("Duration:", duration)

features = extract_features(text, duration=duration)

print("Features:", features)