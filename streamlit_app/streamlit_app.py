"""Simple Streamlit App to play Mandarin syllabes"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import os
from utils.main_functions import play_a_syllable, play_multiple_speakers, AudioFileDataset

# Load and augment dataset
# TODO: Move hardcoded paths and filenames to configs.py
dataset_filename = Path(__file__).parent.parent / "data" / "sample" / "TrATLabelFile.csv"
dataset = AudioFileDataset(dataset_filename)
dataset.preprocess()

# Streamlit UI
st.title("🎧 PinDrill")
st.subheader("A Mandarin Syllable Player")
mode = st.radio("Select mode:", ["Play multiple speakers", "Play a single syllable"])

if mode == "Play multiple speakers":
    syll_choice = st.selectbox("Pick a syllable:", sorted(dataset.df["syllable"].unique()))
    if st.button("Play Now"):
        play_multiple_speakers(dataset.df, syll=syll_choice, st=st)

elif mode == "Play a single syllable":
    row_num = st.number_input("Enter row index (0-based):", min_value=0, max_value=len(dataset.df)-1, step=1)
    show_char = st.checkbox("Show character?")
    if st.button("Play This Syllable"):
        play_a_syllable(dataset.df, n=int(row_num), show_character=show_char, st=st)

# --- Footer with Chinese proverb about learning
st.markdown('---')
st.markdown('**学而不思则罔，思而不学则殆。**  \n*Learning without thought is labor lost; thought without learning is perilous.*  \n— Confucius')
