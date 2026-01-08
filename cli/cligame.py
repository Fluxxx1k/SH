from __future__ import annotations

import datetime
from typing import List, Optional, Tuple, Union, TYPE_CHECKING

import user_settings
from SH2 import take_random
from core.standard_functions import yes_or_no
from core.standard_names_SH import X

if TYPE_CHECKING:
    from core.players.abstract_player import AbstractPlayer
    from core.logs.gamelog import GameLog
    from core.logs.infolog import InfoLog
    from io import TextIOWrapper

from core.games.abstractgame import AbstractGame


class CliGame(AbstractGame):
    """
    class for game in console

    """
    def __init__(self, id: int, name: str, players: list[AbstractPlayer], description: str = None, image: str = None):
        super().__init__(id, name, description, image)


    # def _move(self, prs: AbstractPlayer):


    def take_move(self):
        if self.is_end():
            return self.is_end()
        i = (self.prs.num + 1)% self.globs.COUNT_PLAYERS
        while not self.accept_player(self.globs.PLAYERS[i]):
            i = (i + 1)% self.globs.COUNT_PLAYERS
        self.prs = self.globs.PLAYERS[i]
        if user_settings.VOTE_BY_ONE:
            self.cn = self.prs.choose_chancellor(self.globs.PLAYERS)
            vote_sum = sum([player.vote_for_pair(self.prs, self.globs.PLAYERS[self.cn]) for player in self.players])
            if vote_sum <= 0:
                return 0
        else:
            if yes_or_no(f"Skip? (Skips: {self.skips}): "):
                self.skips += 1
                self.prs.degov()
                print("\n\n\n")
                self.globs.INFO_LOGS.append(InfoLog(X.DBG, "Vote info", f"{self.prs} with {self.cnc} disaccepted",
                                         info2=datetime.datetime.now().strftime(f"{user_settings.DATE_FORMAT} {user_settings.TIME_FORMAT}")))
                return 0
            else:
                self.globs.INFO_LOGS.append(InfoLog(X.DBG, "Vote info", f"{self.prs} with {self.cnc} accepted",
                                         info2=datetime.datetime.now().strftime(f"{user_settings.DATE_FORMAT} {user_settings.TIME_FORMAT}")))
                self.skips = 0
        self.cards = self.take_random(3)



    def start_game(self):
        pass

    def add_player(self, player: AbstractPlayer):
        self.players.append(player)

    def add_players(self, players: list[AbstractPlayer]):
        self.players.extend(players)

    def add_game_log(self, game_log: GameLog):
        self.game_logs.append(game_log)

    def add_info_log(self, info_log: InfoLog):
        self.info_logs.append(info_log)

    def add_game_log_file(self, game_log_file: TextIOWrapper):
        self.game_log_file = game_log_file



    def stop_game(self):
        pass

    def end_game(self):
        pass


    @staticmethod
    def from_dict(data: dict) -> CliGame:
        return CliGame(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            image=data["image"],
        )
