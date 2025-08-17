"""
Helper functions for Pinyin processing and grid generation.
"""
import re
import pandas as pd

def ascii_to_pinyin_full(syllable: str, tone_marks: dict, vowels_ref: list) -> str:
    """
    Convert ASCII Pinyin with tone numbers to marked Pinyin.
    Ensures finals from vowels_ref are correctly processed.
    """
    s = syllable.strip().lower().replace('v', 'ü')
    m = re.match(r"([a-zü]+)([1-5])?$", s)
    if not m:
        return syllable
    base, tone_str = m.groups()
    tone = int(tone_str) if tone_str else 5  # 5 indicates no tone mark

    # If no tone mark needed
    if tone == 5 or tone == 0:
        return base

    # Find which final matches from vowels_ref (longest first)
    match_final = None
    for final in sorted(vowels_ref, key=len, reverse=True):
        # This code works only if longest vowels are checked first
        if base.endswith(final):
            match_final = final
            break

    if not match_final:
        return base  # fallback: nothing matched

    # Tone placement logic
    def place_mark(syl: str, tone: int) -> str:
        """
        Place the tone mark on the appropriate vowel in the syllable.
        Pinyin notation follows the principle of marking the most prominent vowel.
        See: https://www.polyu.edu.hk/bepth/introduction-to-phonetics/spelling-rules-in-pinyin/
        The rule: Mark priority a > e > o > i > u > 'ü'; special-case, the latter in iu/ui.
        """
        if 'iu' in syl:
            idx = syl.index('u')
        elif 'ui' in syl:
            idx = syl.index('i')
        else:
            for vowel in ['a', 'e', 'o', 'i', 'u', 'ü']:
                if vowel in syl:
                    idx = syl.index(vowel)
                    break
        vowel_char = syl[idx]
        return syl[:idx] + tone_marks[vowel_char][tone] + syl[idx+1:]

    return place_mark(base, tone)


def split_pinyin_syllable(syllable, consonants):
    """
    Split a Pinyin syllable into its initial, final, and tone components.
    """
    # Extract tone (last character if it's a digit)
    tone = syllable[-1] if syllable[-1].isdigit() else ''
    base = syllable[:-1] if tone else syllable

    # Match consonant
    initial = ''
    for c in sorted(consonants, key=len, reverse=True):
        if base.startswith(c):
            initial = c
            break

    # Match vowel
    final = base[len(initial):]

    return initial, final, tone


def generate_syllable_grid(consonants, vowels):
    """
    Create a DataFrame with consonants (including '∅') as rows, vowels as columns,
    and syllables (consonant + vowel) as cell values.
    """
    consonants = ["∅"] + consonants  # Use '∅' to represent null initial
    data = {
        vowel: [("" if cons == "∅" else cons) + vowel for cons in consonants]
        for vowel in vowels
    }
    df = pd.DataFrame(data, index=consonants)
    df.index.name = "Initial"
    return df
