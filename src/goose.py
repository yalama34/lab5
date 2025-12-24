from dataclasses import dataclass, field
from .chip import Chip


@dataclass
class Goose:
    name: str
    balance: Chip
    social_class: str
    honk_volume: int

    def __str__(self):
        return f"Гусь {self.name}, баланс: {self.balance}, соц. класс: {self.social_class}, громкость: {self.honk_volume}"


@dataclass
class BaseGoose(Goose):
    balance: Chip = field(default_factory=lambda: Chip(100))
    social_class: str =  "base"
    honk_volume: int = 5

@dataclass
class WarGoose(Goose):
    balance: Chip = field(default_factory=lambda: Chip(100))
    social_class: str = "war"
    honk_volume: int = 6
    steal_value: int = 15

@dataclass
class HonkGoose(Goose):
    balance: Chip = field(default_factory=lambda: Chip(100))
    social_class: str = "honk"
    honk_volume: int = 10

    def __call__(self):
        print(f"Гусь {self.name} издал истошный крик с громкостью {self.honk_volume}. Земля дребезжит от его мощи")

@dataclass
class LeaderGoose(Goose):
    balance: Chip = field(default_factory=lambda: Chip(100))
    social_class: str = "leader"
    honk_volume: int = 9

    def __call__(self):
        print(f"Гусь {self.name} издал победоносный крик с громкостью {self.honk_volume}. Все гуси переключили внимание на лидера")

@dataclass
class TraitorGoose(Goose):
    balance: Chip = field(default_factory=lambda: Chip(100))
    social_class: str = "traitor"
    honk_volume: int = 5
    give_value: int = 15

@dataclass
class MimicGoose(Goose):
    balance: Chip = field(default_factory=lambda: Chip(100))
    social_class: str = "mimic"
    honk_volume: int = 5
    imitating: str | None = field(default_factory=lambda: None)
    original_social_class: str = "mimic"
    original_honk_volume: int = 5
    imitation_steps_left: int = 0

    def start_imitating(self, target_goose, duration: int = 3):
        if self.imitating is not None:
            return None
        self.social_class = target_goose.social_class
        self.honk_volume = target_goose.honk_volume
        if hasattr(target_goose, "steal_value"):
            setattr(self, "steal_value", getattr(target_goose, "steal_value"))
        else:
            if hasattr(self, 'steal_value'):
                delattr(self, 'steal_value')
        if hasattr(target_goose, '__call__'):
            self.__call__ = target_goose.__call__
        self.imitating = target_goose.social_class
        self.imitation_steps_left = duration

    def end_imitating(self):
        if self.imitating is not None:
            self.social_class = self.original_social_class
            self.honk_volume = self.original_honk_volume
            if hasattr(self, 'steal_value'):
                delattr(self, 'steal_value')
            self.imitating = None
            self.imitation_steps_left = 0

    def __call__(self):
        if self.social_class == "honk":
            print(f"Гусь {self.name} имитировал истошный крик с громкостью {self.honk_volume}")
        elif self.social_class == "leader":
            print(f"Гусь {self.name} имитировал победоносный крик с громкостью {self.honk_volume}. Все гуси переключили внимание на псевдо-лидера")


@dataclass
class LenderGoose(Goose):
    balance: Chip = field(default_factory=lambda: Chip(100))
    social_class: str = "lender"
    honk_volume: int = 8
