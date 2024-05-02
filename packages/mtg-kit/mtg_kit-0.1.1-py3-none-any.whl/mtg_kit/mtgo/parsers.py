"""
Collection of tools parse deck files.

Author: José Aniceto
"""

import json
from pathlib import Path
from mtg_kit.models import Deck
from mtg_kit.utils import find_family


def create_decks_json(decks_dir: Path, json_dir: Path):
    """
    Create a JSON file containing all decks.
    :param decks_dir: Folder containing deck files.
    :param json_dir: Output JSON file location.
    """
    # Get new decks
    deck_files = [f for f in decks_dir.iterdir() if f.is_file() and str(f).endswith('.txt')]

    # Parse deck files into deck objects
    decks = []
    for deck_file in deck_files:
        # Create deck object
        deck_name = deck_file.stem
        deck = Deck(name=deck_name)
        deck.color = find_family(deck_name)
        deck.get_decklist_from_txt(deck_file)
        decks.append(deck)

    # Create json
    decks_json = [d.to_dict() for d in decks]

    # Save JSON
    json_file = json_dir / 'decks.json'
    with open(json_file, 'w') as f:
        json.dump(decks_json, f)

    print(f"Decks JSON file created at {json_file}.")
    return decks_json


def get_card_list(json_file: Path):
    """
    Create a list of cards from a JSON files of decks.
    :param json_file: Path to decks JSON file.
    """
    # Open decks
    with open(json_file, 'r') as f:
        decks = json.load(f)

    # Get cards
    cards = []
    for deck in decks:
        for card in deck['mainboard']:
            if card[1] not in cards:
                cards.append(card[1])
        for card in deck['sideboard']:
            if card[1] not in cards:
                cards.append(card[1])

    # Save JSON
    cards_json = json_file.parents[0] / 'cards.json'
    with open(cards_json, 'w') as f:
        json.dump(cards, f)

    print(f"Cards JSON file created at {cards_json}.")
    return cards_json
