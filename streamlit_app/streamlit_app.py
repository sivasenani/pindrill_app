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

row_number_help = """Select the row number - from 0 to 1919 - of the syllable you want to play. 
80 syllables in 4 tones are uttered by six speakers. If you increment the row number you will
hear a different speaker utter the same syllable, till the syllable changes"""
syllable_choice_help = """Pick a syllable from the dropdown to play it uttered by six speakers. 
80 syllables in 4 tones are available."""

# Streamlit UI
st.title("🎧 PinDrill")
st.subheader("A Mandarin Syllable Player")
mode = st.radio("Select mode:", 
                ["Play same syllable uttered by multiple speakers", 
                 "Play a syllable uttered by a single speaker"]
                 )

if mode == "Play same syllable uttered by multiple speakers":
    syll_choice = st.selectbox(
        "Pick a syllable:", 
        sorted(dataset.df["syllable"].unique()), 
        help=syllable_choice_help
        )
    play_multiple_speakers(dataset.df, syll=syll_choice, st=st)

elif mode == "Play a syllable uttered by a single speaker":
    row_num = st.number_input(
        "Enter row index (0-based):", 
        min_value=0, 
        max_value=len(dataset.df)-1, 
        step=1,
        help=row_number_help)
    play_a_syllable(dataset.df, n=int(row_num), show_character=True, st=st)

# --- Footer with Chinese proverb about learning
st.markdown('---')
st.markdown('**学而不思则罔，思而不学则殆。**  \n*Learning without thought is labor lost; thought without learning is perilous.*  \n— Confucius')
