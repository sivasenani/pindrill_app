"""This file contains the reference lists for tones, consonants, vowels and tone_maarks."""

tones_ref = [
    # Note: neutral tone 0 is added
    "0", "1", "2", "3", "4"
]


consonants_ref = [
    # Sorted longest-first by consonant length for greedy matching
    # Note: "ng" is not used as an initial in standard Mandarin; included here only if needed for completeness
    # Note: handle zero-initial syllables (vowel‑only) on the fly in code

    "zh", "ch", "sh",
    "b", "p", "m", "f",
    "d", "t", "n", "l",
    "g", "k", "h",
    "j", "q", "x",
    "r", "z", "c", "s",
    "y", "w"
]


vowels_ref = [
    # Sorted longest-first by vowel length for greedy matching
    # Note: "uong" is not used in standard Mandarin though it is omitted
    # Note: handle ü as 'v' on the fly in code (normalize 'v' <-> 'ü')

    "iang", "uang", "iong", "uong",
    "iao", "ian", "ing", "uai", "uan", "ang", "eng", "ong", "üan",
    "ai", "ei", "ao", "ou", "an", "en", "er", "ia", "ie", "in", "iu", "ua", "uo", "ui", "un", "üe", "ün",
    "a", "o", "e", "i", "u", "ü"
]


# Tone mark mappings - neutral tone is 0, rest are 1 to 4
tone_marks = {
    'a': ['a', 'ā', 'á', 'ǎ', 'à'],
    'e': ['e', 'ē', 'é', 'ě', 'è'],
    'i': ['i', 'ī', 'í', 'ǐ', 'ì'],
    'o': ['o', 'ō', 'ó', 'ǒ', 'ò'],
    'u': ['u', 'ū', 'ú', 'ǔ', 'ù'],
    'ü': ['ü', 'ǖ', 'ǘ', 'ǚ', 'ǜ']
}
