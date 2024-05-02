from pathlib import Path
import typer
from typing_extensions import Annotated
from mtg_kit.utils import setup_dir
from mtg_kit.mtgo import exporter, organizer, parsers, bulk_manage


# Configuration
STRIP_CHARS = ['#T1', '#T2', ' !']
BANLIST = ['Monastery Swiftspear', 'Aarakocra Sneak', 'Stirring Bard', 'Underdark Explorer', 'Vicious Battlerager'
           'Prophetic Prism', 'Disciple of the Vault', 'Galvanic Relay']

# Folders
base_dir = Path().absolute()
data_dir = base_dir / 'data'
decks_dir = data_dir / 'mtgo-decks'
default_decks_json = data_dir / 'decks.json'


app = typer.Typer()


def cli():
    app()


@app.command()
def export(valid: bool = True, json_path: Path = data_dir):
    """Auto export decks from MTGO into .txt files.

    If `valid=True` it separates removes deck files that are invalid (i.e., decks with banned cards).
    Creates a JSON file containing all exported decks.
    """
    # Set up directories
    setup_dir(decks_dir)

    # Export decks
    exporter.auto_export(str(decks_dir) + '\\')

    # Organize decks
    organizer.clean_file_names(decks_dir, chars_to_strip=STRIP_CHARS)
    if valid:
        organizer.remove_invalid_decks(decks_dir, banlist=BANLIST)

    # Parse deck files and create JSON
    parsers.create_decks_json(decks_dir, json_path)


@app.command()
def organize(fmt: str = 'pauper'):
    """Organize exported decks."""
    organizer.clean_file_names(decks_dir, chars_to_strip=STRIP_CHARS)
    organizer.remove_invalid_decks(decks_dir, banlist=BANLIST)


@app.command()
def parse_decks(decks_path: Path = decks_dir, json_path: Path = data_dir):
    """Parse deck files exported decks."""
    # Create decks JSON file
    parsers.create_decks_json(decks_path, json_path)

    # Create cards JSON file
    parsers.get_card_list(data_dir / 'decks.json')


@app.command()
def bulk_change_card(
        current: str,
        new: str,
        decks_json: Path = default_decks_json,
        dry: Annotated[bool, typer.Option(help="Run without making any changes")] = False
):
    bulk_manage.bulk_change_card(current, new, decks_json, dry=dry)
