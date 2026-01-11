from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any

from core import utils

if TYPE_CHECKING:
    from io import TextIOWrapper
    from core.players.abstract_player import AbstractPlayer
    from core.logs.gamelog import GameLog
    from core.logs.infolog import InfoLog


import json



class GlobalStorage:
    def __init__(self, name: str,
                 info_logs: list[InfoLog] = None,
                 game_logs: list[GameLog] = None,
                 count_players: int = None,
                 players: list[AbstractPlayer] = None,
                 roles: list[str] = None,
                 hitler: int | None = None,
                 stalin: int | None = None,
                 purged: set[AbstractPlayer] = None,
                 gulag: int | None = None,
                 killed: int | None = None,
                 black: int = 0,
                 red: int = 0,
                 bots: list[int] = None,
                 active_game: bool = True,
                 hit_chancellor: bool = False,
                 hit_chancellor_stal_president: bool = False,
                 hit_caput: bool = False,
                 ):
        self.name: str = name
        self.INFO_LOGS: list[InfoLog] = info_logs or []
        self.GAME_LOGS: list[GameLog] = game_logs or []
        # noinspection PyTypeChecker
        self.COUNT_PLAYERS: int = count_players or None
        self.PLAYERS: list[AbstractPlayer] = players or []
        self.ROLES: list[str] = roles or []
        self.HITLER: int | None = hitler or None
        self.STALIN: int | None = stalin or None
        self.PURGED: set[AbstractPlayer] = purged or set()
        self.GULAG: int | None = gulag or None
        self.KILLED: int | None = killed or None
        self.BLACK: int = black
        self.RED: int = red
        self.BOTS: list[int] = bots or []
        self.ACTIVE_GAME: bool = active_game
        self.HIT_CHANCELLOR: bool = hit_chancellor
        self.HIT_CHANCELLOR_STAL_PRESIDENT: bool = hit_chancellor_stal_president
        self.HIT_CAPUT: bool = hit_caput

    def get(self, key: str, default: Any = None) -> Optional[Any]:
        return self.__dict__.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __contains__(self, item: str) -> bool:
        return item in self.__dict__

    def __getitem__(self, item: str) -> Any:
        return self.__dict__[item]
    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value
    def __delitem__(self, key: str) -> None:
        if key in base_dict:
            raise ValueError(f"Cannot delete base attribute: {key}")
        del self.__dict__[key]

    def is_active(self):
        return self.ACTIVE_GAME
    def set_active(self, value: bool):
        self.ACTIVE_GAME = value

    def __bool__(self):
        return self.__dict__ != base_dict

    def __str__(self):
        return f"GlobalStorage({self.name})"

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other: GlobalStorage) -> bool:
        return self.__dict__ == other.__dict__

    def __ne__(self, other: GlobalStorage) -> bool:
        return self.__dict__ != other.__dict__

    def __hash__(self) -> int:
        return hash(self.name)

    def copy(self) -> GlobalStorage:
        from copy import deepcopy
        new_obj = GlobalStorage(self.name)
        for key, value in self.__dict__.items():
            new_obj.__dict__[key] = deepcopy(value)
        return new_obj

    __copy__ = __deepcopy__ = copy

    def to_json(self) -> str:
        gs_dict = {}
        for i, j in self.__dict__.items():
            if i in base_dict:
                gs_dict[i] = utils.update_obj_to_json(j)
        return json.dumps(gs_dict)

    def from_json(self, json_str: str) -> None:
        self.__dict__ = json.loads(json_str)

    def save_to_file(self, file: str | TextIOWrapper) -> None:
        """
        Save the GlobalStorage object to a file.

        :param file: The file path or TextIOWrapper object to save the data to.
        :type file: str | TextIOWrapper
        """
        if isinstance(file, str):
            with open(file, 'w+', encoding='utf-8') as file:
                file.write(self.to_json())
        elif isinstance(file, TextIOWrapper):
            file.write(self.to_json())

    def load_from_file(self, file: str | TextIOWrapper) -> None:
        """
        Load the GlobalStorage object from a file.

        :param file: The file path or TextIOWrapper object to load the data from.
        :type file: str | TextIOWrapper
        """
        if isinstance(file, str):
            with open(file, 'r', encoding='utf-8') as file:
                self.from_json(file.read())
        elif isinstance(file, TextIOWrapper):
            self.from_json(file.read())



base_dict = GlobalStorage('base_name').__dict__


if __name__ == '__main__':
    from core.logs.gamelog import GameLog
    from core.logs.infolog import InfoLog
    gs = GlobalStorage('test name')
    gs.set('test key', 'test value')
    print(gs)
    print(gs['test key'])
    print(gs.get('test key'))
    print(gs.get('test2', 'default'))
    print('test' in gs)
    print('test2' in gs)
    # del gs['test']
    print(gs)
    # gs.PURGED = Exception('test exception')
    # gs.INFO_LOGS = tuple([InfoLog(info_type='test', info_name='test', info1='test', info2='test') for _ in range(10)])
    print(gs.__dict__)
    print(gs.to_json())
