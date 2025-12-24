from dataclasses import dataclass, field
from .chip import Chip
from typing import Dict


@dataclass
class Player:
    name: str
    balance: Chip
    social_class: str
    debt: list[Dict[str, Chip]] = field(default_factory=list)

    def pay_debt(self):
        if not self.debt:
            return None
        messages = []
        for debt in self.debt[:]:
            interest = debt["interest"]
            remaining = debt["remaining"]
            if self.balance.value >= interest.value:
                self.balance -= interest
                messages.append(f"Игрок {self.name} выплатил проценты: {interest}")
            else:
                lost = self.balance.value
                self.balance = Chip(0)
                messages.append(f"Игрок {self.name} не смог оплатить проценты! Списано всё ({lost})")
            if self.balance.value > round(remaining.value / 15):
                part_pay = round(remaining.value / 15)
                self.balance -= part_pay
                remaining -= part_pay
                if remaining.value > 0:
                    messages.append(f"Игрок {self.name} выплатил часть долга: {part_pay}")
                else:
                    messages.append(f"Игрок {self.name} выплатил долг")

        return "; ".join(messages) if messages else None

    def __str__(self):
        return f"{self.name}, баланс - {self.balance}, класс - {self.social_class}"

@dataclass
class PoorPlayer(Player):
    balance: Chip = field(default_factory=lambda: Chip(50))
    social_class: str = "poor"
    win_chance: float = 0.3
    attack_chance: float = 0.65


@dataclass
class MiddlePlayer(Player):
    balance: Chip = field(default_factory=lambda: Chip(100))
    social_class: str = "middle"
    win_chance: float = 0.5
    attack_chance: float = 0.5

@dataclass
class RichPlayer(Player):
    balance: Chip = field(default_factory=lambda: Chip(300))
    social_class: str = "rich"
    win_chance: float = 0.65
    attack_chance: float = 0.2
