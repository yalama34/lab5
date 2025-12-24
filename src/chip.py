from functools import total_ordering

@total_ordering
class Chip:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Chip):
            return Chip(self.value + other.value)
        elif isinstance(other, int):
            return Chip(self.value + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Chip):
            return Chip(max(self.value - other.value, 0))
        elif isinstance(other, int):
            return Chip(max(self.value - other, 0))
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Chip):
            return Chip(self.value * other.value)
        elif isinstance(other, int):
            return Chip(self.value * other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Chip):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Chip):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented

    def __repr__(self):
        return f'Chip({self.value})'

    def __str__(self):
        return str(self.value)