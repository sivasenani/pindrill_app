"""Streamlit App for Playing Mandarin Syllables"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import streamlit as st
from streamlit_option_menu import option_menu
from utils.main_functions import AudioFileDataset, play_a_syllable, play_multiple_speakers
from utils.reference_lists import easy_consonants, medium_consonants, hard_consonants, very_hard_consonants, easy_vowels, medium_vowels, hard_vowels, very_hard_vowels
from utils.helping_functions import generate_syllable_grid

# Load and augment dataset
# TODO: Move hardcoded paths and filenames to configs.py
dataset_filename = Path(__file__).parent.parent / "data" / "sample" / "TrATLabelFile.csv"
dataset = AudioFileDataset(dataset_filename)
dataset.preprocess()

# Helping variables
row_number_help = (
	"Select the row number of the syllable you want to play. If you increment the "
	"row number you will hear a different speaker utter the same syllable, till the "
	"syllable changes."
)
syllable_choice_help = (
	"Pick a syllable from the dropdown to play it uttered by six speakers."
)

# Streamlit app layout
st.title("🎧 PinDrill")
st.subheader("A Mandarin Syllable Player")

# Sidebar for menu options. We want the following menu options:
# Explore Syllables, Practice Listening, Listening Test, Practice Speaking, Speaking Test, About App
# Each of the five sections will have five tabs each: Easy, Medium, Hard, Very Hard and Shuffle
st.sidebar.title("Menu")


with st.sidebar:
	selected = option_menu(
		"Menu",
		["Explore Syllables", "Practice Listening", "Listening Test", "Practice Speaking", "Speaking Test", "About App"],
		icons=["book", "headphones", "clipboard-check", "mic", "check2-circle", "info-circle"],
		menu_icon="cast",
		default_index=0,
		orientation="vertical"
	)

tab_labels = ["Easy", "Medium", "Hard", "Very Hard", "Shuffle"]

if selected == "Explore Syllables":
	tabs = st.tabs(tab_labels)
	for i, tab in enumerate(tabs):
		with tab:
			st.write(f"Explore Syllables — {tab_labels[i]}")
			if tab_labels[i] == "Easy":
				temp_df = generate_syllable_grid(easy_consonants, easy_vowels)
				st.dataframe(temp_df, use_container_width=True)
				st.write("Ready to explore these syllables?")

                # If yes is checked, start exploring
				if st.checkbox("Yes", key=f"yes_start_{tab_labels[i]}"):
					del temp_df  # Clear the temporary DataFrame
					mode = st.radio("Select mode:", 
					 ["Same syllable uttered by multiple speakers", 
					   "One syllable uttered by a single speaker"],
					   key=f"mode_{tab_labels[i]}",
				 )
					if mode == "Same syllable uttered by multiple speakers":
						syll_choice = st.selectbox(
                            "Pick a syllable:", 
                            sorted(dataset.df_easy["syllable"].unique()), 
                            help=syllable_choice_help
                            )
						play_multiple_speakers(dataset.df_easy, syll=syll_choice, st=st)
						
					elif mode == "One syllable uttered by a single speaker":
						row_num = st.number_input(
                            "Enter row index (0-based):", 
                            min_value=0, 
                            max_value=len(dataset.df_easy)-1, 
                            step=1,
                            help=row_number_help)
						indx_number = dataset.df_easy.index[int(row_num)]
						play_a_syllable(dataset.df_easy, n=indx_number, show_character=True, st=st)

			elif tab_labels[i] == "Medium":
				temp_df = generate_syllable_grid(medium_consonants, medium_vowels)
				st.dataframe(temp_df, use_container_width=True)
				st.write("Ready to explore these syllables?")
				# If yes is checked, start exploring
				if st.checkbox("Yes", key=f"yes_start_{tab_labels[i]}"):
					del temp_df  # Clear the temporary DataFrame
					mode = st.radio("Select mode:", 
					 ["Same syllable uttered by multiple speakers", 
					   "One syllable uttered by a single speaker"],
					   key=f"mode_{tab_labels[i]}",
				 )
					if mode == "Same syllable uttered by multiple speakers":
						syll_choice = st.selectbox(
							"Pick a syllable:", 
							sorted(dataset.df_medium["syllable"].unique()), 
							help=syllable_choice_help
						)
						play_multiple_speakers(dataset.df_medium, syll=syll_choice, st=st)
						
					elif mode == "One syllable uttered by a single speaker":
						row_num = st.number_input(
							"Enter row index (0-based):", 
							min_value=0, 
							max_value=len(dataset.df_medium)-1, 
							step=1,
							help=row_number_help)
						indx_number = dataset.df_medium.index[int(row_num)]
						play_a_syllable(dataset.df_medium, n=indx_number, show_character=True, st=st)

			elif tab_labels[i] == "Hard":
				temp_df = generate_syllable_grid(hard_consonants, hard_vowels)
				st.dataframe(temp_df, use_container_width=True)
				st.write("Ready to explore these syllables?")
				# If yes is checked, start exploring
				if st.checkbox("Yes", key=f"yes_start_{tab_labels[i]}"):
					del temp_df  # Clear the temporary DataFrame
					mode = st.radio("Select mode:", 
						["Same syllable uttered by multiple speakers", 
						 "One syllable uttered by a single speaker"],
					   key=f"mode_{tab_labels[i]}",
					)
					if mode == "Same syllable uttered by multiple speakers":
						syll_choice = st.selectbox(
							"Pick a syllable:", 
							sorted(dataset.df_hard["syllable"].unique()), 
							help=syllable_choice_help
						)
						play_multiple_speakers(dataset.df_hard, syll=syll_choice, st=st)
					elif mode == "One syllable uttered by a single speaker":
						row_num = st.number_input(
							"Enter row index (0-based):", 
							min_value=0, 
							max_value=len(dataset.df_hard)-1, 
							step=1,
							help=row_number_help)
						indx_number = dataset.df_hard.index[int(row_num)]
						play_a_syllable(dataset.df_hard, n=indx_number, show_character=True, st=st)

			elif tab_labels[i] == "Very Hard":
				temp_df = generate_syllable_grid(very_hard_consonants, very_hard_vowels)
				st.dataframe(temp_df, use_container_width=True)
				st.write("Ready to explore these syllables?")
				# If yes is checked, start exploring
				if st.checkbox("Yes", key=f"yes_start_{tab_labels[i]}"):
					del temp_df  # Clear the temporary DataFrame
					mode = st.radio("Select mode:", 
						["Same syllable uttered by multiple speakers", 
						 "One syllable uttered by a single speaker"],
					   key=f"mode_{tab_labels[i]}",
					)
					if mode == "Same syllable uttered by multiple speakers":
						syll_choice = st.selectbox(
							"Pick a syllable:", 
							sorted(dataset.df_very_hard["syllable"].unique()), 
							help=syllable_choice_help
						)
						play_multiple_speakers(dataset.df_very_hard, syll=syll_choice, st=st)
					elif mode == "One syllable uttered by a single speaker":
						row_num = st.number_input(
							"Enter row index (0-based):", 
							min_value=0, 
							max_value=len(dataset.df_very_hard)-1, 
							step=1,
							help=row_number_help)
						indx_number = dataset.df_very_hard.index[int(row_num)]
						play_a_syllable(dataset.df_very_hard, n=indx_number, show_character=True, st=st)

			elif tab_labels[i] == "Shuffle":
				mode = st.radio("Select mode:", 
					 ["Same syllable uttered by multiple speakers", 
					   "One syllable uttered by a single speaker"],
					   key=f"mode_{tab_labels[i]}",
				 )
				if mode == "Same syllable uttered by multiple speakers":
					syll_choice = st.selectbox(
						"Pick a syllable:", 
						sorted(dataset.df["syllable"].unique()), 
						help=syllable_choice_help
						)
					play_multiple_speakers(dataset.df, syll=syll_choice, st=st)
				elif mode == "One syllable uttered by a single speaker":
					row_num = st.number_input(
						"Enter row index (0-based):", 
						min_value=0, 
						max_value=len(dataset.df)-1, 
						step=1,
						help=row_number_help)
					indx_number = dataset.df[int(row_num)]
					play_a_syllable(dataset.df, n=indx_number, show_character=True, st=st)

elif selected == "Practice Listening":
	tabs = st.tabs(tab_labels)
	for i, tab in enumerate(tabs):
		with tab:
			st.write(f"Practice Listening — {tab_labels[i]}")
			if tab_labels[i] == "Easy":
				# Combine the easy consonants and vowels into a syllable list and display those in a grid
				temp_df = generate_syllable_grid(easy_consonants, easy_vowels)
				st.dataframe(temp_df, use_container_width=True)

			elif tab_labels[i] == "Medium":
				# Combine the medium consonants and vowels into a syllable list and display those in a grid
				temp_df = generate_syllable_grid(medium_consonants, medium_vowels)
				st.dataframe(temp_df, use_container_width=True)

			elif tab_labels[i] == "Hard":
				# Combine the hard consonants and vowels into a syllable list and display those in a grid
				temp_df = generate_syllable_grid(hard_consonants, hard_vowels)
				st.dataframe(temp_df, use_container_width=True)

			elif tab_labels[i] == "Very Hard":
				# Combine the very hard consonants and vowels into a syllable list and display those in a grid
				temp_df = generate_syllable_grid(very_hard_consonants, very_hard_vowels)
				st.dataframe(temp_df, use_container_width=True)

			elif tab_labels[i] == "Shuffle":
				st.info("Content under development. Stay tuned for updates!")

elif selected == "Listening Test":
	tabs = st.tabs(tab_labels)
	for i, tab in enumerate(tabs):
		with tab:
			st.write(f"Listening Test — {tab_labels[i]}")
			if tab_labels[i] == "Easy":
				st.info("Content under development. Stay tuned for updates!")
			elif tab_labels[i] == "Medium":
				st.info("Content under development. Stay tuned for updates!")
			elif tab_labels[i] == "Hard":
				st.info("Content under development. Stay tuned for updates!")
			elif tab_labels[i] == "Very Hard":
				st.info("Content under development. Stay tuned for updates!")
			elif tab_labels[i] == "Shuffle":
				st.info("Content under development. Stay tuned for updates!")

elif selected == "Practice Speaking":
	tabs = st.tabs(tab_labels)
	for i, tab in enumerate(tabs):
		with tab:
			st.write(f"Practice Speaking — {tab_labels[i]}")
			if tab_labels[i] == "Easy":
				st.info("This is some time away. Let us see.")
			elif tab_labels[i] == "Medium":
				st.info("This is some time away. Let us see.")
			elif tab_labels[i] == "Hard":
				st.info("This is some time away. Let us see.")
			elif tab_labels[i] == "Very Hard":
				st.info("This is some time away. Let us see.")
			elif tab_labels[i] == "Shuffle":
				st.info("This is some time away. Let us see.")

elif selected == "Speaking Test":
	tabs = st.tabs(tab_labels)
	for i, tab in enumerate(tabs):
		with tab:
			st.write(f"Speaking Test — {tab_labels[i]}")
			if tab_labels[i] == "Easy":
				st.info("This is some time away. Let us see.")
			elif tab_labels[i] == "Medium":
				st.info("This is some time away. Let us see.")
			elif tab_labels[i] == "Hard":
				st.info("This is some time away. Let us see.")
			elif tab_labels[i] == "Very Hard":
				st.info("This is some time away. Let us see.")
			elif tab_labels[i] == "Shuffle":
				st.info("This is some time away. Let us see.")


elif selected == "About App":
	st.markdown("""
## 🎉 About PinDrill

Welcome to **PinDrill** — your interactive playground for Mandarin pronunciation! 🇨🇳✨

- 🏆 **Track Your Progress:** PinDrill keeps tabs on your learning journey. Watch your skills level up as you go!
- 🎯 **Graded Learning:** Four challenge zones await: Easy, Medium, Hard, and Very Hard. Plus, hit **Shuffle** for a wild ride through all levels!
- 📹 **Coming Soon:** Get ready to record your own audio and test your pronunciation against the pros. 
			 
Ready to drill, and skill up your Mandarin? Let’s go! 🚀
			 
Want the source code and data files? Check out: https://github.com/sivasenani/pindrill_app 
""")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.markdown(
    """
    <small style='color:gray'>
    This app is being built with ❤️ by Siva Senani Nori. Hope you find it helpful!
    </small>
    """,
    unsafe_allow_html=True
)

# --- Footer with Chinese proverb about learning
st.markdown('---')
st.markdown('**学而不思则罔，思而不学则殆。**  \n*Learning without thought is labor lost; thought without learning is perilous.*  \n— Confucius')