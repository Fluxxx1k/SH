from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any, Union

from cli.user_color_settings import CRITICAL
from core import utils

if TYPE_CHECKING:
    from io import TextIOWrapper
    from Players.abstract_player import AbstractPlayer
    from core.gamelog import GameLog
    from core.infolog import InfoLog


import json



class GlobalStorage:
    def __init__(self, name: str):
        self.name: str = name
        self.INFO_LOGS: list[InfoLog] = []
        self.GAME_LOGS: list[GameLog] = []
        # noinspection PyTypeChecker
        self.COUNT_PLAYERS: int = None
        self.PLAYERS: list[AbstractPlayer] = []
        self.ROLES: list[str] = []
        self.HITLER: int | None = None
        self.STALIN: int | None = None
        self.PURGED: set[AbstractPlayer] = set()
        self.GULAG: int | None = None
        self.KILLED: int | None = None
        self.CARDS: dict[str, int] = {"BLACK": 0, "RED": 0}
        self.BOTS: list[int] = []
        self.ACTIVE_GAME: bool = True

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
        return self.name

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
    from core.gamelog import GameLog
    from core.infolog import InfoLog
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
