from src.casino import Casino
from src.player import PoorPlayer
from src.chip import Chip


def test_player_registration():
    casino = Casino()
    casino.register_player(name="Alice", social_class="poor")
    assert len(casino.players) == 1
    assert casino.players[0].name == "Alice"
    assert casino.players[0].balance.value == 50


def test_bankruptcy_removal():
    casino = Casino()
    player = PoorPlayer(name="Bob")
    player.balance = Chip(0)
    casino.players.append(player)

    casino.remove_bankrupt_players()
    assert len(casino.players) == 0