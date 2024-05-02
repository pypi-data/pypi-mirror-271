"""
Functions to bulk edit deck files

Author: José Aniceto
"""

import json
from pathlib import Path


def bulk_change_card(current_card: str, new_card: str, json_file: Path, dry: bool = False):

    # Log info
    if dry:
        print('This is a dry run. No cards are actually changed.')
    print('Searching cards...')
    print(f'Looking for: {current_card}')
    print(f'Substituting for: {new_card}')

    # Load decks file
    with open(json_file, 'r') as f:
        decks = json.load(f)

    # Make change in all decks
    mainboard_hits = 0
    sideboard_hits = 0
    for i, deck in enumerate(decks):
        for j, card in enumerate(deck['mainboard']):
            if card[1] == current_card:
                print(f"Found on deck mainboard: {deck['name']}")
                mainboard_hits += 1
                decks[i]['mainboard'][j][1] = new_card

        for j, card in enumerate(deck['sideboard']):
            if card[1] == current_card:
                print(f"Found on deck sideboard: {deck['name']}")
                sideboard_hits += 1
                decks[i]['sideboard'][j][1] = new_card

    # Rewrite decks
    if not dry:
        with open(json_file, 'w') as f:
            json.dump(decks, f)

    # Summarise run
    print(f"Run completed. {current_card} was found in:")
    print(f" - Mainboard hits: {mainboard_hits}")
    print(f" - Sideboard hits: {sideboard_hits}")
