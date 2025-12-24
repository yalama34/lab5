from src.chip import Chip

def test_chip_addition():
    chip1 = Chip(10)
    chip2 = Chip(20)
    result = chip1 + chip2
    assert result.value == 30

def test_chip_subtraction():
    chip = Chip(50)
    result = chip - 15
    assert result.value == 35
    assert result.value >= 0