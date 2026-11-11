"""
Signal two: the style signal, implemented in milestone 4.

Signal one measures predictability. This one measures text shape, without
understanding a word.

The style score averages three measurements after converting each to 0–1.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics
import unicodedata

import config


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three raw measures ──────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence lengths vary relative to their mean (pstdev / mean).

    Fewer than two sentences with words gives zero. style_signal flips the
    direction so that more variation gives a lower AI-looking score.
    """
    lengths = [len(words(sentence)) for sentence in sentences(text)]
    lengths = [length for length in lengths if length]
    if len(lengths) < 2:
        return 0.0
    return statistics.pstdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """
    Unique lowercase words over total words; zero for wordless text.

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    tokens = words(text)
    return len(set(tokens)) / len(tokens) if tokens else 0.0


def punctuation_density(text: str) -> float:
    """
    Unicode punctuation characters divided by total text characters.

    Return zero for empty input; count every Unicode punctuation category.
    """
    if not text:
        return 0.0
    return sum(unicodedata.category(char).startswith("P") for char in text) / len(text)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    Mean of three aligned 0–1 features. Higher points toward AI.

    No words gives 0.5. With fewer than two sentences, only the length part
    gets 0.5. The calculations and sample scores are in README.md.
    """
    if not words(text):
        return 0.5
    sentence_count = sum(bool(words(sentence)) for sentence in sentences(text))
    spread_score = 0.5 if sentence_count < 2 else 1.0 - min(sentence_length_spread(text), 1.0)
    repetition_score = 1.0 - type_token_ratio(text)
    punctuation_score = 1.0 - min(punctuation_density(text) / config.STYLE_PUNCTUATION_DENSITY_CEILING, 1.0)
    return round((spread_score + repetition_score + punctuation_score) / 3.0, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
