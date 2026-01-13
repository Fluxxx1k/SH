from __future__ import annotations

from typing import Literal, Iterable

from WebsiteEasiest.data.database_py.games import get_data_of_game
from WebsiteEasiest.data.database_py.players import get_data_for_player
from WebsiteEasiest.logger import logger
from core.players.abstract_player import AbstractPlayer


class WebPlayer(AbstractPlayer):
    def __init__(self, index, name, role):
        super().__init__(index, name, role)
        self.game_name = get_data_for_player(self.name)[1]['game']

    def president(self, cards: str | list[str], cnc: "AbstractPlayer"):
        pass

    def chancellor(self, cards: str, prs: "AbstractPlayer", words, veto):
        pass

    def president_said_after_chancellor(self, *, cards: str, cnc: "AbstractPlayer", ccg: str, cps: str, ccs: str,
                                        ccp: str) -> str:
        pass

    def check_cards(self, cards: str) -> str:
        pass

    def check_player(self) -> tuple[int, str]:
        pass

    def purge_another(self, purge_type: str, votes: dict[int, int] = None) -> int:
        vote = self._voted_for_who()
        return vote

    def place_another(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        vote = self._voted_for_who()
        return vote

    def choose_chancellor(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int | None:
        vote = self._voted_for_who()
        return vote

    def vote_for_pair(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        game_data = get_data_of_game(self.game_name)
        if not game_data[0]:
            raise ValueError(f"Game {self.game_name} not found: {game_data[1]}")
        votes = game_data[1].get('votes', {}).get(self.name, {})
        vote_type = votes.get('type', None)
        if vote_type is None or vote_type == 'player':
            return 0
        if vote_type == 'pass':
            return 0
        if vote_type == 'yes':
            return 1
        if vote_type == 'no':
            return -1
        logger.error(f"Unknown vote type {vote_type} for player {self.name} in game {self.game_name}")
        return 0

    def _voted_for_who(self, index: bool = True) -> str | None | int:
        game_data = get_data_of_game(self.game_name)
        if not game_data[0]:
            raise ValueError(f"Game {self.game_name} not found: {game_data[1]}")
        votes = game_data[1].get('votes', {}).get(self.name, {})
        vote_type = votes.get('type', None)
        if vote_type is None or vote_type in {'pass', 'yes', 'no'}:
            return None
        if vote_type == 'player':
            if index:
                try:
                    return game_data[1]['players'].index(votes.get('target', ''))
                except ValueError:
                    return None
            return votes.get('target', None)
        logger.error(f"Unknown vote type {vote_type} for player {self.name} in game {self.game_name}")
        return None
