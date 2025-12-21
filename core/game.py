from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Any
if TYPE_CHECKING:
    from io import TextIOWrapper
    from Players.abstract_player import AbstractPlayer
    from core.gamelog import GameLog
    from core.infolog import InfoLog



class Game:
    def __init__(self, id: int, name: str, description: str, image: str):
        self.id = id
        self.name = name
        self.description = description
        self.image = image

    def __str__(self):
        return f"{self.__name__}(id={self.id}, name='{self.name}', description='{self.description}', image='{self.image}')"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.image == other.image
        )

    def __hash__(self):
        return hash((self.id, self.name, self.description, self.image))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
        }

    @staticmethod
    def from_dict(data: dict) -> Game:
        return Game(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            image=data["image"],
        )
