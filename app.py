import streamlit as st
import joblib
import pandas as pd
import os

from utils.parse_transcripts import parse_cha_file
from utils.extract_features import extract_features

# load trained model
MODEL_PATH = "Backend/model/alzheimer_model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    st.error(f"Trained model not found at {MODEL_PATH}. Please run train_model.py first.")
    st.stop()

st.title("Speech-Based Alzheimer Risk Classification")

uploaded_file = st.file_uploader("Upload Transcript (.cha)", type="cha")

if uploaded_file is not None:

    with open("temp.cha", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract speech text and duration
    text, duration = parse_cha_file("temp.cha")

    # Extract features using duration
    features = extract_features(text, duration=duration)

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
        "speaking_rate"
    ]

    features_df = pd.DataFrame([features], columns=columns)

    prediction = model.predict(features_df)[0]
    probabilities = model.predict_proba(features_df)[0]
    confidence = max(probabilities) * 100

    if prediction == 0:
        st.success("Prediction: Control (No Alzheimer Risk)")
    else:
        st.error("Prediction: Alzheimer Risk Detected")

    st.write(f"Confidence: {confidence:.2f}%")

    st.subheader("Extracted Speech Features")
    st.dataframe(features_df)

    st.subheader("Visual Feature Comparison")
    st.bar_chart(features_df.T)