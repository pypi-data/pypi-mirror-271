import requests
from mtg_kit.utils import MTG_FORMATS


def get_card(query: str) -> list:
    """
    Runs a card search on the Scryfall API.

    Get a list of cards that match a given query to the Scryfall database.

    Args:
        query (str): The query string, using Scryfall syntax.

    Returns:
        list: A list of Scryfall card objects that match the query.
    """
    cards = []
    page = 1
    while True:
        url = f"https://api.scryfall.com/cards/search?q={query}&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch cards: {response.text}")
            break
        data = response.json()
        cards.extend([card for card in data['data']])

        if not data['has_more']:
            break
        page += 1

    return cards


def get_card_printings(card_name: str) -> list | None:
    """
    Search for all printints of a given card.

    Gets a list of card objects that correspond to all printings of a given card.

    Args:
        card_name: The card name to search for.

    Returns:
        list or None: The list of printings (card objects) that match the searched card name. If search fails returns
        None.
    """
    card = get_card(card_name)[0]  # assume the first card is the wanted one
    prints_url = card['prints_search_uri']

    # Fetch all printings
    response = requests.get(prints_url)
    data = response.json()

    # Check if the printings fetch was successful
    if response.status_code == 200:
        card_printings = [cp for cp in data['data']]
    else:
        print(f"Failed to retrieve card printings: {data['details']}")
        card_printings = None

    return card_printings


def get_banned_cards(fmt: str) -> list[str]:
    """
    Get a list of cards banned in a given format.

    Uses the Scryfall API to get a list of card names which are banned in a specified format.

    Args:
        fmt (str): The MtG format.

    Returns:
        list: A list of card names.
    """
    if fmt not in MTG_FORMATS:
        raise ValueError(f'Error: format (fmt) must be one of {MTG_FORMATS}')
    card_objs = get_card(f'banned:{fmt}')
    return [c['name'] for c in card_objs]


def card_exists(card_name: str) -> bool:
    """
    Check if a specific card name exists in the Scryfall API.

    This function queries the Scryfall 'cards/named' API endpoint with an exact match search for the provided card name.
    It returns a boolean indicating the existence of the card.

    Args:
        card_name (str): The name of the MTG card to search for.

    Returns:
        bool: True if the card exists in the Scryfall database, False otherwise.

    Raises:
        requests.RequestException: An error from the `requests` library indicating a problem with the network or the
        fetch operation.
    """
    url = "https://api.scryfall.com/cards/named"
    params = {'exact': card_name}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # The card exists
            return True
        else:
            # If the card is not found, Scryfall will usually respond with a 404
            return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == '__main__':
    # Get Pauper banlist
    pauper_banlist = get_banned_cards('pauper')
    print(pauper_banlist)

    # Search card
    r = get_card_printings('Demand Answers')
    print(r)
