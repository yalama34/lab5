from enum import Enum
from .chip import Chip

class PlayerType(Enum):
    poor = "poor"
    middle = "middle"
    rich = "rich"

class GooseType(Enum):
    base = "base"
    war = "war"
    honk = "honk"
    leader = "leader"
    traitor = "traitor"
    mimic = "mimic"
    lender = "lender"

player_min_bets = {
    "poor": Chip(30),
    "middle": Chip(25),
    "rich": Chip(50)
}