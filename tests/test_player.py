from src.player import PoorPlayer, MiddlePlayer
from src.chip import Chip


def test_poor_player_initialization():
    player = PoorPlayer(name="Test")
    assert player.name == "Test"
    assert player.balance.value == 50
    assert player.social_class == "poor"
    assert player.win_chance == 0.3


def test_debt_payment():
    player = MiddlePlayer(name="Test")
    player.debt.append({
        "amount": Chip(100),
        "interest": Chip(3),
        "remaining": Chip(100)
    })
    player.balance = Chip(20)

    message = player.pay_debt()
    assert message is not None
    assert player.balance.value == 10