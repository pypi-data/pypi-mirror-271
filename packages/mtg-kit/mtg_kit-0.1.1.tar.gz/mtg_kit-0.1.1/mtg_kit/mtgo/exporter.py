"""
Script to automate exporting MTGO decks to file.
Automates the mouse and keyboard movement required to export decks from MTGO.
Organizes decks into folders

Notes:
- You must have MTGO client open.
- You must be on the Collection page.
- You must select the first deck to export.
- Only decks in the selected deck category are exported.
- You can not change windows or move cursor while the script is running.

Author: José Aniceto
"""

import sys
from pathlib import Path
import pyautogui
import pyperclip
from tqdm import tqdm
from mtg_kit.utils import setup_dir


def focus_mtgo_window():
    """Focus the MTGO window by clicking the title bar (top)."""
    pyautogui.click(338, 9, button='left')


def auto_export(filepath):
    """Automate mouse and keyboard movement necessary to export decks from MTGO into .txt files."""
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True

    # Check if first deck is selected
    prep = input('Have you selected the first deck you want to export? ([y]/n): ')
    if prep not in ['', 'y', 'yes', 'Y', 'Yes']:
        sys.exit('Please select the first deck you want to export and run the script again.')

    # How many decks to save
    decks_to_save = input('How many decks would you like to export? (300): ')
    if decks_to_save == '':
        deck_number = 300
    else:
        try:
            deck_number = int(decks_to_save)
        except ValueError:
            sys.exit('Please enter an integer number or leave blank to use the default value.')

    print('Initiating exporting.\nMove the mouse to the upper-left corner to cancel.')

    # Focus MTGO window
    focus_mtgo_window()

    # Scroll over decks and export
    with tqdm(total=deck_number) as pbar:
        deck_count = 1
        while True:
            pbar.update()

            # Press context menu key
            pyautogui.hotkey('shift', 'f10')

            # Use keyboard to select Export from the context menu
            pyautogui.typewrite(['down', 'down', 'down', 'down', 'enter'])

            # Use keyboard to select path
            if filepath:
                pyautogui.press('left')
                pyperclip.copy(filepath)
                pyautogui.hotkey("ctrl", "v")

            # Use keyboard to select file type and save
            pyautogui.typewrite(['tab', 'down', 'down', 'enter', 'enter'])

            # End job
            if deck_count == deck_number:
                break

            # Focus MTGO window
            focus_mtgo_window()

            # Press down to go to next deck
            pyautogui.press('down')

            deck_count += 1


if __name__ == '__main__':
    decks_path_ = Path().absolute().parents[1]
    setup_dir(decks_path_)
    auto_export(decks_path_)
