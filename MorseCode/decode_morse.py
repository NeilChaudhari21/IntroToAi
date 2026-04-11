from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
from functools import lru_cache

from wordfreq import zipf_frequency


LETTER_TO_MORSE = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
}


@dataclass(frozen=True)
class WordOption:
    word: str
    morse: str
    freq: float


@dataclass(frozen=True)
class PathState:
    words: tuple[str, ...]
    remaining: str
    score: float


def word_to_morse(word: str) -> str:
    return "".join(LETTER_TO_MORSE[ch] for ch in word)


def load_dictionary(path: Path) -> list[str]:
    words: set[str] = set()
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        word = raw.strip().lower()
        if re.fullmatch(r"[a-z]+", word):
            words.add(word)
    return sorted(words)


def rank_next_words(stream: str, dictionary: list[str], top_n: int = 20) -> list[WordOption]:
    clean_stream = "".join(ch for ch in stream if ch in {".", "-"})
    options: list[WordOption] = []

    for word in dictionary:
        morse = word_to_morse(word)
        if clean_stream.startswith(morse):
            options.append(
                WordOption(
                    word=word,
                    morse=morse,
                    freq=zipf_frequency(word, "en", wordlist="best"),
                )
            )

    options.sort(key=lambda item: (-item.freq, len(item.word), item.word))
    return options[:top_n]


def phrase_score(words: tuple[str, ...]) -> float:
    if not words:
        return 0.0

    score = 0.0
    for index, word in enumerate(words):
        freq = zipf_frequency(word, "en", wordlist="best")
        score += 2.0 * freq

        if len(word) <= 2:
            score -= 1.4
        elif len(word) >= 5:
            score += 0.4

        if index > 0 and words[index - 1] == word:
            score -= 4.0

        if index > 0:
            bigram = f"{words[index - 1]} {word}"
            bigram_freq = zipf_frequency(bigram, "en", wordlist="best")
            score += 4.0 * bigram_freq
            if bigram_freq < 1.5:
                score -= 1.75

        if index > 1:
            trigram = f"{words[index - 2]} {words[index - 1]} {word}"
            trigram_freq = zipf_frequency(trigram, "en", wordlist="best")
            score += 2.0 * trigram_freq
            if trigram_freq < 1.0:
                score -= 1.0

    # Prefer fewer fragmented sentences.
    score -= 1.05 * len(words)
    score -= 1.1 * sum(1 for word in words if len(word) <= 2)
    return score


def beam_search_paths(
    stream: str,
    dictionary: list[str],
    top_words: int = 20,
    beam_width: int = 250,
    max_words: int = 25,
) -> list[PathState]:
    clean_stream = "".join(ch for ch in stream if ch in {".", "-"})
    if not clean_stream:
        return []

    initial = PathState(words=(), remaining=clean_stream, score=0.0)
    beam: list[PathState] = [initial]

    dictionary_tuple = tuple(dictionary)

    @lru_cache(maxsize=None)
    def ranked_candidates(remaining: str) -> tuple[WordOption, ...]:
        return tuple(rank_next_words(remaining, list(dictionary_tuple), top_n=top_words))

    while beam:
        next_beam: list[PathState] = []
        for state in beam:
            if not state.remaining:
                next_beam.append(state)
                continue

            candidates = ranked_candidates(state.remaining)
            for candidate in candidates:
                if not state.remaining.startswith(candidate.morse):
                    continue

                new_words = state.words + (candidate.word,)
                new_remaining = state.remaining[len(candidate.morse) :]
                new_score = phrase_score(new_words)

                # Favor states that consume more of the stream while still remaining plausible.
                new_score += 0.05 * (len(clean_stream) - len(new_remaining))

                next_beam.append(
                    PathState(
                        words=new_words,
                        remaining=new_remaining,
                        score=new_score,
                    )
                )

        if not next_beam:
            break

        next_beam.sort(key=lambda state: (state.score, -len(state.remaining), " ".join(state.words)), reverse=True)
        beam = next_beam[:beam_width]

        # Stop once all top states have consumed the stream or we've hit the max word count.
        if all(not state.remaining for state in beam):
            break
        if all(len(state.words) >= max_words for state in beam):
            break

    return sorted(
        beam,
        key=lambda state: (state.score, -len(state.remaining), " ".join(state.words)),
        reverse=True,
    )


def stepwise_decode(stream: str, dictionary: list[str], top_n: int = 20) -> None:
    remaining = "".join(ch for ch in stream if ch in {".", "-"})
    chosen_words: list[str] = []

    while remaining:
        options = rank_next_words(remaining, dictionary, top_n=top_n)
        if not options:
            print("No dictionary word matches the remaining Morse prefix.")
            print(f"Remaining Morse: {remaining}")
            return

        print()
        if chosen_words:
            print("Chosen so far:", " ".join(chosen_words))
        print(f"Remaining Morse: {remaining}")
        print(f"Top {len(options)} next-word candidates:")
        for index, option in enumerate(options, start=1):
            print(f"{index:>2}. {option.word}\tzipf={option.freq:.3f}\tmorse={option.morse}")

        choice = input("Choose a word number, type a word, or press Enter to stop: ").strip().lower()
        if not choice:
            return

        if choice.isdigit():
            selected_index = int(choice) - 1
            if selected_index < 0 or selected_index >= len(options):
                print("Invalid selection.")
                continue
            selected = options[selected_index]
        else:
            selected = next((option for option in options if option.word == choice), None)
            if selected is None:
                print("That word is not a valid candidate for this prefix.")
                continue

        chosen_words.append(selected.word)
        remaining = remaining[len(selected.morse):]

    print()
    print("Decoded sentence:", " ".join(chosen_words))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactively test Morse word sequences by ranking the next valid word by English frequency."
    )
    parser.add_argument(
        "morse",
        help="Continuous Morse stream containing only dots and dashes.",
    )
    parser.add_argument(
        "--dict",
        dest="dict_path",
        default=r"c:\Users\neilc\Downloads\dictionary.txt",
        help="Path to the dictionary file.",
    )
    parser.add_argument(
        "--top",
        dest="top_n",
        type=int,
        default=20,
        help="How many candidate words to show each step.",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatically choose the top-ranked word at each step.",
    )
    parser.add_argument(
        "--beam",
        action="store_true",
        help="Search multiple word paths and print the best full-sentence candidates.",
    )
    parser.add_argument(
        "--beam-width",
        type=int,
        default=250,
        help="How many partial sentence paths to keep during beam search.",
    )
    args = parser.parse_args()

    dictionary = load_dictionary(Path(args.dict_path))
    if not dictionary:
        raise SystemExit("Dictionary is empty or contains no valid words.")

    if args.auto:
        remaining = "".join(ch for ch in args.morse if ch in {".", "-"})
        sentence: list[str] = []
        while remaining:
            options = rank_next_words(remaining, dictionary, top_n=args.top_n)
            if not options:
                print("No further matches found.")
                break
            selected = options[0]
            sentence.append(selected.word)
            remaining = remaining[len(selected.morse):]
        print(" ".join(sentence))
        return

    if args.beam:
        results = beam_search_paths(
            args.morse,
            dictionary,
            top_words=args.top_n,
            beam_width=args.beam_width,
        )

        if not results:
            print("No candidate paths found.")
            return

        print(f"Found {len(results)} path candidates. Top {min(args.top_n, len(results))}:")
        for index, state in enumerate(results[: args.top_n], start=1):
            sentence = " ".join(state.words)
            remainder_note = f" | remaining={state.remaining}" if state.remaining else ""
            print(f"{index:>2}. score={state.score:8.3f} | {sentence}{remainder_note}")
        return

    stepwise_decode(args.morse, dictionary, top_n=args.top_n)


if __name__ == "__main__":
    main()
