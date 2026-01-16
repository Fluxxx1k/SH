from __future__ import annotations

from WebsiteEasiest.web_core.games_players_classes.webplayer import WebPlayer
from core.games.basegame import BaseGame
from WebsiteEasiest.settings.website_settings import get_roles
games_dict: dict[str, WebGame] = {}


class WebGame(BaseGame):
    def __init__(self, game_name: str, game_data: dict):
        game_data['roles'] = get_roles(game_data['current_players'])
        self.roles = game_data['roles']
        super().__init__(game_name, [WebPlayer(i, game_data['players'][i], self.roles[i]) for i in range(game_data['current_players'])])
        games_dict[game_name] = self
