from user_color_settings import WARNING
class Cards(str):
    def __init__(self, cards: str) -> None:
        cards = cards.strip().upper()
        self.cards = cards
        if cards == 'VETO':
            print(f"{WARNING} ")
        if not set(cards).issubset(POSSIBLE_CARDS):
            raise ValueError(f"Invalid cards: {cards}")
        super().__init__(cards)

POSSIBLE_CARDS: set[str] = set("BRX")
