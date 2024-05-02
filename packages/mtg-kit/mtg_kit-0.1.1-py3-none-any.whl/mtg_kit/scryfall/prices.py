from mtg_kit.models import Price
from mtg_kit.scryfall.search import get_card_printings


def get_prices(card_name: str) -> list[Price]:
    """
    Get prices of all printings of a given card.

    Returns a list of Price objects for all printings found in Scryfall for a given card.

    Args:
        card_name (str): The card to search for prices.

    Returns:
        list[Price]: A list of Price objects for all printings of the given card.
    """
    # Get card info
    card_printings = get_card_printings(card_name)

    # Return a list of prices dictionary
    prices = []
    for card_printing in card_printings:
        try:
            price = Price(
                card_name=card_printing['name'],
                set=card_printing['set'].upper(),
                foil=False,
                price=float(card_printing['prices']['tix']),
                currency='tix'
            )
            prices.append(price)
        except TypeError as e:
            # print('Error:', e)
            pass
    return prices


if __name__ == '__main__':
    card = 'Rancor'
    p = get_prices(card)
    print(p)
