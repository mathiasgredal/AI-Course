from __future__ import annotations

from enum import Enum, auto


class StateTypes(Enum):
    CLEAN = auto()
    DIRTY = auto()
    UNKNOWN = auto()

    def __repr__(self):
        return self.name


class Action(Enum):
    SUCK = auto()
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    NO_OP = auto()

    def __repr__(self):
        return self.name
# --
# A B
# C D
# --
class Location(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    CURRENT = auto()
    UNKNOWN = auto()

    def __repr__(self):
        return self.name

    def allowed_moves(self) -> tuple[Action, ...]:
        always_allowed = (Action.NO_OP,)
        if self == Location.A:
            return Action.DOWN, Action.RIGHT, *always_allowed
        if self == Location.B:
            return Action.DOWN, Action.LEFT, *always_allowed
        if self == Location.C:
            return Action.UP, Action.RIGHT, *always_allowed
        if self == Location.D:
            return Action.UP, Action.LEFT, *always_allowed
        return always_allowed

    def perform_move(self, move: Action) -> Location:
        """ Returns the resulting location after performing the move"""
        if move not in (Action.RIGHT, Action.LEFT, Action.UP, Action.DOWN):
            return self

        return _moves[move][self]


_right = {
    Location.A: Location.B,
    Location.B: Location.UNKNOWN,
    Location.C: Location.D,
    Location.D: Location.UNKNOWN
}

_left = {
    Location.A: Location.UNKNOWN,
    Location.B: Location.A,
    Location.C: Location.UNKNOWN,
    Location.D: Location.C
}

_up = {
    Location.A: Location.UNKNOWN,
    Location.B: Location.UNKNOWN,
    Location.C: Location.A,
    Location.D: Location.B
}

_down = {
    Location.A: Location.C,
    Location.B: Location.B,
    Location.C: Location.UNKNOWN,
    Location.D: Location.UNKNOWN
}

_moves = {
    Action.DOWN: _down,
    Action.UP: _up,
    Action.LEFT: _left,
    Action.RIGHT: _right
}
