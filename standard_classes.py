from colors import RESET_TEXT, END
from user_color_settings import WARNING, CARDS_COLORS
from user_settings import IS_PRINT_SMALL_INFO, IS_PRINT_FULL_INFO
#from utils import coloring

class Cards(str):
    def __init__(self, cards: str) -> None:
        cards = cards.strip().upper()
        self.cards = cards
        self.colored_cards = self.coloring_cards()
        if cards == 'VETO':
            print(f"{WARNING}IDK, VETO ")
        if not set(cards).issubset(POSSIBLE_CARDS):
            raise ValueError(f"Invalid cards: {cards}")
        # super().__init__()
    def __matmul__(self, other=None) -> str:
        return self.coloring_cards()
    def coloring_cards(self=None, cards: "str | Cards" = None, *,
                       print_errors: bool = IS_PRINT_FULL_INFO,
                       is_print: bool = IS_PRINT_SMALL_INFO) -> str:
        s = ''
        if cards is None:
            cards = self.cards
        for card in cards:
            try:
                s += CARDS_COLORS[card] + card + RESET_TEXT
            except KeyError:
                if print_errors:
                    print(f"{WARNING}Invalid card: {repr(card)}{END}")
                elif is_print:
                    print(f"{WARNING}Invalid card{END}")
                s += card
            except Exception as err:
                if print_errors:
                    print(f"{WARNING}UNKNOWN ERROR: {err} \n Card: {repr(card)}{END}")
                elif is_print:
                    print(f"{WARNING}UNKNOWN ERROR{END}")
                s += card
        return s


POSSIBLE_CARDS: set[str] = set("BRX")

if __name__ == "__main__":
    a = Cards("RBX")
    b = Cards("RBX")
    print(a == b)
    print(a != b)
    print(a != "RBX")
    print(a == "RBX")
    print(a.colored_cards)
    print(Cards.coloring_cards(None, 'P'))
    print(Cards('BB')@'12')
    print(0)