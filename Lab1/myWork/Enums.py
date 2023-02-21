from enum import Enum, auto


class States(Enum):
    CLEAN = auto()
    DIRTY = auto()
    UNKNOWN = auto()


class Action(Enum):
    SUCK = auto()
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    NO_OP = auto()


class Location(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    CURRENT = auto()
    UNKNOWN = auto()

    def allowed_moves(self) -> tuple[Action, ...]:
        always_allowed = Action.NO_OP, Action.SUCK
        if self == Location.A:
            return Action.DOWN, Action.RIGHT, *always_allowed
        if self == Location.B:
            return Action.DOWN, Action.LEFT, *always_allowed
        if self == Location.C:
            return Action.UP, Action.RIGHT, *always_allowed
        if self == Location.D:
            return Action.UP, Action.LEFT, *always_allowed
        return always_allowed
