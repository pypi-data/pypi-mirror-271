"""
General utility functions
Data and utility functions related with Magic the Gathering

Author: José Aniceto
"""

from pathlib import Path


def setup_dir(dir_name):
    """Create directory if it doesn't exist."""
    dir_path = Path(dir_name)
    dir_path.mkdir(parents=True, exist_ok=True)


# List of color family names
MTG_FORMATS = [
    'standard', 'future', 'historic', 'timeless', 'gladiator', 'pioneer', 'explorer', 'modern', 'legacy', 'pauper',
    'vintage', 'penny', 'commander', 'oathbreaker', 'standardbrawl', 'brawl', 'alchemy', 'paupercommander', 'duel',
    'oldschool', 'premodern', 'predh',
]


# List of color family names
FAMILIES = [
    'white', 'blue', 'black', 'red', 'green', 'selesnya', 'orzhov', 'boros', 'azorius', 'dimir', 'rakdos', 'golgari',
    'izzet', 'simic', 'gruul', 'naya', 'esper', 'grixis', 'jund', 'bant', 'abzan', 'temur', 'jeskai', 'mardu', 'sultai',
    'glint', 'dune', 'ink', 'whitch', 'yore', 'domain', 'colorless'
]


def find_family(deck_name: str) -> str:
    """Given a deck name, try to find the deck family."""
    for family in FAMILIES:
        if family in deck_name.lower():
            return family
