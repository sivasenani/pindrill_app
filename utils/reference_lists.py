"""This file contains the reference lists for tones, consonants, vowels and tone_maarks."""

tones_ref = ["0", "1", "2", "3", "4"]

# Consonants
easy_consonants = ["p", "m", "f", "n", "l", "k", "s", "y"]
medium_consonants = ["b", "d", "g", "h", "t", "w"]
hard_consonants = ["sh", "r", "z", "c"]
very_hard_consonants = ["j", "q", "x", "zh", "ch"]
# Sorted longest-first by consonant length for greedy matching.
# Note: "ng" is not used as an initial in standard Mandarin; included here only
# if needed for completeness.
# Note: handle zero-initial syllables (vowel‑only) on the fly in code.
consonants_ref = sorted((easy_consonants + 
                   medium_consonants + 
                   hard_consonants + 
                   very_hard_consonants),
                   key=len, reverse=True)


# Vowels
easy_vowels = ["a", "o", "i", "u", "an", "in", "un", "ing"]
medium_vowels = ["e", "ai","ua", "uo", "en", "ang", "eng", "ian", "ong"]
hard_vowels = ["ü", "ei", "ao", "ou", "er", "ia",  "iu", "ün", "uan"]
very_hard_vowels = ["ie", "iao", "üe", "uai", "ui", "üan", "iang", "uang", "iong", "uong"]
# Sorted longest-first by vowel length for greedy matching.
# Note: "uong" is not used in standard Mandarin, though it is included for
# completeness. It is omitted in most practical cases.
# Note: handle ü as 'v' on the fly in code (normalize 'v' <-> 'ü').
vowels_ref = sorted((easy_vowels + 
                     medium_vowels + 
                     hard_vowels + 
                     very_hard_vowels), 
                     key=len, reverse=True)


# Tone mark mappings - neutral tone is 0, rest are 1 to 4
tone_marks = {
    'a': ['a', 'ā', 'á', 'ǎ', 'à'],
    'e': ['e', 'ē', 'é', 'ě', 'è'],
    'i': ['i', 'ī', 'í', 'ǐ', 'ì'],
    'o': ['o', 'ō', 'ó', 'ǒ', 'ò'],
    'u': ['u', 'ū', 'ú', 'ǔ', 'ù'],
    'ü': ['ü', 'ǖ', 'ǘ', 'ǚ', 'ǜ']
}
