"""Contains the functions required to play sounds in the Toy Streamlit App"""

from collections import defaultdict
import os
import random
from pathlib import Path
import re
import pandas as pd
from utils.reference_lists import consonants_ref, vowels_ref, tone_marks, tones_ref
from utils.helping_functions import ascii_to_pinyin_full, split_pinyin_syllable

# TODO: Move hardcoded paths and filenames to configs.py
data_dir = Path(__file__).parent.parent / "data" / "sample"

# Play a single syllable
def play_a_syllable(df: pd.DataFrame, n: int = None, show_character: bool = False, st=None) -> None: 
    """Play a single syllable audio."""
    row = df.sample(1).iloc[0] if n is None else df.iloc[n]
    folder_num = int(row["fold"])
    file_name = row["Name"]
    pinyin_char = row["pinyin"]
    file_path = data_dir / "TrAT" / f"TrAT-fold{folder_num}" / file_name
    if st:
        st.audio(file_path)
        if show_character:
            st.write(pinyin_char)
    else:
        if show_character: print(f"Playing audio for {pinyin_char}")
        # Play audio without Streamlit
        os.startfile(file_path)
        # wait for a key to be pressed to continue
        input("Press Enter to continue...")


# Play multiple speakers for a syllable
def play_multiple_speakers(df: pd.DataFrame, syll: str = None, st=None) -> None:
    """Play audio for multiple speakers for a given syllable."""
    if syll is None:
        syll = random.choice(df["syllable"].unique())
    matching_indices = df.index[df["syllable"] == syll].tolist()
    if st:
        st.write(f"Playing all speakers for syllable: {syll}")
    else:
        print(f"Playing all speakers for syllable: {syll}")
    for indx in sorted(matching_indices):
        speaker = df.iloc[indx]["speaker"]
        pinyin_char = df.iloc[indx]["pinyin"]
        if st:
            st.write(f"{pinyin_char} by {speaker}:")
        else:
            print(f"{pinyin_char} by {speaker}:")
        play_a_syllable(df, indx, show_character=False, st=st) 

# Write a Class to load the dataset, analyse it, and then preprocess it
class AudioFileDataset:
    def __init__(self, df_filename):
        """Initialize the dataset."""

        self.df = pd.read_csv(df_filename)
        print(f"Audio File Dataset loaded with {len(self.df)} entries. \nColumns: {list(self.df.columns)}\n")
        
    def preprocess(self):
            """Preprocess the dataset and further analyze."""
        
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

            print(f"Preprocessing complete. Dataset now has {len(self.df)} entries with columns: "
                  f"{list(self.df.columns)}\n")

    def save_processed(self, output_filename):
        """Save the processed dataset to a CSV file."""

        self.df.to_csv(output_filename, index=False)
        print(f"Processed dataset saved to {output_filename}")

    def analyze(self):
        """Analyze the dataset for insights."""

        print("Analyzing dataset...\n")
        unique_syllables = self.df["syllable"].unique().tolist()
        unique_speakers = self.df["speaker"].unique().tolist()
        print(f"Total unique syllables: {len(unique_syllables)}")
        print(f"Total unique speakers: {len(unique_speakers)}")
        speakers_per_syllable = self.df.groupby('syllable')['speaker'].nunique().sort_values(ascending=False)
        print("Speakers per syllable:")
        print(speakers_per_syllable)
        print()

        select_columns = ["syllable", "initial_consonant", "final_vowel", "tone"]
        df1 = self.df[select_columns].drop_duplicates()
        # Add a "base", ie syllable without tone to check whether every syllable occurs in all the tones
        df1['base'] = df1['syllable'].apply(lambda x: re.match(r'([a-z]+)(\d)', x).group(1))
        present_tones = df1["tone"].unique().tolist()
        present_consonants = df1["initial_consonant"].unique().tolist()
        present_vowels = df1["final_vowel"].unique().tolist()
        print(f"{present_tones = } \n{present_consonants = } \n{present_vowels = }\n")

        missing_tones = list(set(tones_ref) - set(present_tones))
        missing_consonants = list(set(consonants_ref) - set(present_consonants))
        missing_vowels = list(set(vowels_ref) - set(present_vowels))
        print(f"{missing_tones = } \n{missing_consonants = } \n{missing_vowels = }")

        syllables_by_consonant = defaultdict(list)
        for cons in present_consonants:
            syllables_by_consonant[cons] = df1[df1["initial_consonant"] == cons].base.unique().tolist()
            print(f"{cons}({len(syllables_by_consonant[cons])}): {syllables_by_consonant[cons]}")
        
        # Extract unique base and tone to a separate df
        unique_df = df1[['base', 'tone']].drop_duplicates().reset_index(drop=True)
        print(f"{len(unique_df) = }")
        # Group by the base syllable and count unique tones
        tone_counts = unique_df.groupby("base")["tone"].nunique().reset_index(name="tone_count")
        print(tone_counts)


# Dataset analysis and preprocessing:
if __name__ == "__main__":
    print("This module is not intended to be run directly. Use it as a library in the Streamlit app.")
    # TODO: Move hardcoded paths and filenames to configs.py
    dataset_filename = Path.cwd() / "TrATLabelFile.csv"
    output_filename = Path.cwd() / "TrATLabelFile_processed.csv"

    dataset = AudioFileDataset(dataset_filename)
    dataset.preprocess()
    dataset.save_processed(output_filename)
    dataset.df.sample(5)
    dataset.analyze()
    print("\n -------------------- \n")
    print("Playing audio for syllable: ")
    play_a_syllable(dataset.df, show_character=True)
    print("\nUse the play_multiple_speakers function to play all speakers for a syllable.")
    play_multiple_speakers(dataset.df)
