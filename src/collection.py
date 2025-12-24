from .player import Player
from .goose import Goose
from .chip import Chip
from typing import Dict
import logging

class BaseCollection:
    def __init__(self, items = None):
        self.items = list(items) if items else []
    def __getitem__(self, key: int | slice):
        if isinstance(key, slice):
            return self.__class__(self.items[key])
        return self.items[key]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.items})"

    def __contains__(self, item):
        return item in self.items


class PlayerCollection(BaseCollection):
    @property
    def players(self):
        return self.items

    def append(self, player):
        if not isinstance(player, Player):
            raise TypeError("Можно добавлять только объекты класса Player.")
        self.players.append(player)

    def remove_player(self, player_name: str):
        try:
            self.players.remove(player_name)
        except:
            print(f"Игрок {player_name} не найден")

    def __str__(self):
        output = ""
        player_num = 1
        for player in self.players:
            output += f"Игрок #{player_num} {player.name}, баланс - {player.balance}, класс - {player.social_class}\n"
            player_num += 1
        return output

class GooseCollection(BaseCollection):
    @property
    def geese(self):
        return self.items

    def append(self, goose):
        if not isinstance(goose, Goose):
            raise TypeError("Можно добавлять только объекты класса Goose.")
        self.geese.append(goose)

    def __str__(self):
        output = ""
        goose_num: int = 1
        for goose in self.geese:
            output += f"Гусь #{goose_num} {goose.name}, баланс - {goose.balance}, класс - {goose.social_class}\n"
            goose_num += 1
        return output



class CasinoBalance:
    def __init__(self, data = None):
        self.data: Dict[str, Chip] = dict(data) if data is not None else {}
        self.logger = logging.getLogger("CasinoBalance")
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def __setitem__(self, key: str, value: Chip):
        old_value = self.data.get(key, None)
        self.data[key] = value
        if old_value:
            self.logger.info(f"{key}: баланс изменён с {str(old_value)} на {str(value)}")

    def __getitem__(self, key: str):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

