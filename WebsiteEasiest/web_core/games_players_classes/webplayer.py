from __future__ import annotations

import time
from typing import Literal, Iterable

from WebsiteEasiest.data.database_py.games import get_data_of_game
from WebsiteEasiest.data.database_py.players import get_data_of_player
from WebsiteEasiest.logger import logger
from core.players.abstract_player import AbstractPlayer


class WebPlayer(AbstractPlayer):
    def __init__(self, index, name, role):
        super().__init__(index, name, role)
        self.game_name = get_data_of_player(self.name)[1]['game']
        self._vote_yesno = None
        self._vote_player = None
        self._cards_action = None
        self._cards = None

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
        return self._voted_for_who_in_index()

    def place_another(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        return self._voted_for_who_in_index()

    def choose_chancellor(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int | None:
        return self._voted_for_who_in_index()


    def _voted_for_who(self) -> str:
        """Get player's vote target"""
        while self._vote_player is None:
            logger.debug(f"Player {self.name} in game {self.game_name} has not voted yet, waiting 10 seconds")
            time.sleep(10)
        return self.get_vote_player()

    def _voted_for_who_in_index(self) -> int:
        """Get player's vote target index"""
        return self.players.index(self._voted_for_who())

    def vote_for_pair(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        game_data = get_data_of_game(self.game_name)
        if not game_data[0]:
            raise ValueError(f"Game {self.game_name} not found: {game_data[1]}")
        votes = game_data[1].get('votes', {}).get(self.name, {})
        vote_type = votes.get('type', None)
        if vote_type != 'yesNo':
            logger.warning(f"Player {self.name} in game {self.game_name} voted for pair with unknown vote type {vote_type} and target {votes.get('target', None)}, timestamp: {votes.get('timestamp', None)}")
            return 0
        if vote_type == 'pass':
            return 0
        if vote_type == 'yes':
            return 1
        if vote_type == 'no':
            return -1
        logger.error(f"Unknown vote type {votes.get('target', None)} for player {self.name} in game {self.game_name}: {votes}")
        return 0


    def has_voted(self) -> bool:
        """Check if player has submitted a vote"""
        return getattr(self, '_vote_yesno', None) is not None

    def get_vote(self) -> Literal[-1, 0, 1]:
        """Get and clear player's vote (1=YES, -1=NO, 0=PASS)"""
        vote = self._vote_yesno
        self._vote_yesno = None
        return vote if vote is not None else 0

    def set_vote(self, vote: Literal[-1, 0, 1]):
        """Set player's vote from web interface"""
        self._vote_yesno = vote


    def set_vote_player(self, vote: str):
        """Set player's vote target from web interface"""
        self._vote_player = vote

    def has_voted_player(self) -> bool:
        """Check if player has submitted a vote target"""
        return getattr(self, '_vote_player', None) is not None

    def get_vote_player(self) -> str | None:
        """Get and clear player's vote target"""
        vote = self._vote_player
        self._vote_player = None
        return vote

    def set_cards_action(self, cards: str):
        """Set player's action from web interface"""
        self._cards = cards

    def get_cards_action(self) -> str | None:
        """Get and clear player's action"""
        cards = self._cards
        self._cards = None
        return cards

    def has_cards_action(self) -> bool:
        """Check if player has submitted an action"""
        return getattr(self, '_cards', None) is not None
