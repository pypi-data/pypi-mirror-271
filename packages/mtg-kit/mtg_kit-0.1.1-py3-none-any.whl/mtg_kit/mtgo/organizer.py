"""
Collection of tools to clean and organize deck files exported from MTGO.

Author: José Aniceto
"""

from pathlib import Path
from typing import List


def clean_file_names(decks_dir: Path, chars_to_strip: List[str]):
    """Run through all deck files in a folder and clean deck filename."""

    deck_files = [f for f in decks_dir.iterdir() if f.is_file() and str(f).endswith('.txt')]

    for filepath in deck_files:
        filename = filepath.stem  # file name without extension

        for char in chars_to_strip:
            filename = filename.strip().strip('!').replace(char, '').strip()
        new_filename = filename + '.txt'
        new_filepath = decks_dir / new_filename

        if filepath != new_filepath:
            try:
                filepath.rename(new_filepath)
            except FileExistsError:
                print(f"File already exists: {new_filepath}")


def remove_invalid_decks(decks_dir: Path, banlist: List[str] = None):
    """Remove invalid deck files i.e., decks with banned cards."""
    deck_files = [f for f in decks_dir.iterdir() if f.is_file() and str(f).endswith('.txt')]

    # Remove deck files with banned cards
    for deck_file in deck_files:
        with open(deck_file, 'r') as f:
            data = f.read()

        if any(card in data for card in banlist):
            deck_file.unlink()


if __name__ == '__main__':
    decks_path_ = Path().absolute().parents[1] / 'data' / 'mtgo-decks'

    # Clean deck names
    STRIP_CHARS = ['#T1', '#T2', ' !']
    clean_file_names(decks_path_, chars_to_strip=STRIP_CHARS)

    # Remove invalid decks
    BANLIST = ['Monastery Swiftspear', 'Aarakocra Sneak', 'Stirring Bard', 'Underdark Explorer', 'Vicious Battlerager']
    remove_invalid_decks(decks_path_, banlist=BANLIST)
