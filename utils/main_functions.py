"""
Contains the functions required to play sounds in the Toy Streamlit App.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from collections import defaultdict
import os
import random
import re
import pandas as pd
from utils.reference_lists import (consonants_ref, vowels_ref, tone_marks, tones_ref, 
                                   easy_consonants,  easy_vowels, medium_consonants, 
                                   medium_vowels, hard_consonants, hard_vowels, 
                                   very_hard_consonants, very_hard_vowels
)
from utils.helping_functions import ascii_to_pinyin_full, split_pinyin_syllable

# TODO: Move hardcoded paths and filenames to configs.py
# Data directory for sample files
data_dir = Path(__file__).parent.parent / "data" / "sample"

# Play a single syllable
def play_a_syllable(df: pd.DataFrame, n: int = None, show_character: bool = False, st=None) -> None: 
    """Play a single syllable audio."""
    row = df.sample(1).iloc[0] if n is None else df.loc[n]
    folder_num = int(row["fold"])
    file_name = row["Name"]
    pinyin_char = row["pinyin"]
    file_path = data_dir / "TrAT" / f"TrAT-fold{folder_num}" / file_name
    if st:
        if show_character:
            st.write(pinyin_char)
        st.audio(file_path)
    else:
        # Play audio without Streamlit
        os.startfile(file_path)


# Play multiple speakers for a syllable
def play_multiple_speakers(df: pd.DataFrame, syll: str = None, st=None) -> None:
    """Play audio for multiple speakers for a given syllable."""
    if syll is None:
        syll = random.choice(df["syllable"].unique())
    matching_indices = df.index[df["syllable"] == syll].tolist()

    if st:
        st.write(f"Playing all speakers for syllable: {syll}")
    for indx in sorted(matching_indices):
        speaker = df.loc[indx]["speaker"]
        pinyin_char = df.loc[indx]["pinyin"]
        selected_syll = df.loc[indx]["syllable"]
        
        if st:
            st.write(f"{pinyin_char} by {speaker}:")
        play_a_syllable(df, indx, show_character=False, st=st) 

# Write a Class to load the dataset, analyse it, and then preprocess it.
class AudioFileDataset:
    def __init__(self, df_filename):
        """Initialize the dataset."""

        self.df = pd.read_csv(df_filename)
        
    def preprocess(self):
        """
        Preprocess the dataset and further analyze.
        Extracts syllable and speaker, splits syllable into initial consonant,
        final vowel, and tone, and generates filtered datasets for each level.
        """
        # Extract syllable and speaker from the 'Name' column
        self.df[['syllable', 'speaker']] = self.df['Name'].str.extract(r'^(.*?)_(.*?)_')

        # Split 'syllable' column into initial consonant, final vowel, and tone
        self.df[['initial_consonant', 'final_vowel', 'tone']] = self.df['syllable'].apply(
            lambda s: pd.Series(split_pinyin_syllable(s, consonants_ref))
        )
        # Replace NaN or empty strings in 'consonant' with the zero initial symbol
        self.df["initial_consonant"] = self.df["initial_consonant"].fillna("").replace(r"^\s*$", "Ø", regex=True)

        # Apply the function to the 'syllable' column and store result in 'pinyin'
        self.df["pinyin"] = self.df["syllable"].apply(
            lambda s: pd.Series(ascii_to_pinyin_full(s, tone_marks, vowels_ref))
        )

        # Convert 'tone' to string for consistency
        self.df["tone"] = self.df["tone"].astype(str)

        # Generate the dataset for easy, medium, hard, and very hard levels
        easy_consonants_with_null = ["Ø"] + easy_consonants
        self.df_easy = self.df[
            self.df['initial_consonant'].isin(easy_consonants_with_null) |
            self.df['final_vowel'].isin(easy_vowels)
        ]
        self.df_medium = self.df[
            self.df['initial_consonant'].isin(medium_consonants) |
            self.df['final_vowel'].isin(medium_vowels)
        ]
        self.df_hard = self.df[
            self.df['initial_consonant'].isin(hard_consonants) |
            self.df['final_vowel'].isin(hard_vowels)
        ]
        self.df_very_hard = self.df[
            self.df['initial_consonant'].isin(very_hard_consonants) |
            self.df['final_vowel'].isin(very_hard_vowels)
        ]
