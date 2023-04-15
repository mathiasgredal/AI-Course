from enum import Enum, auto


class SAStates(Enum):
    CostaRica = auto()
    Panama = auto()
    Colombia = auto()
    Venezuela = auto()
    Guyana = auto()
    Suriname = auto()
    GuyaneFR = auto()
    Ecuador = auto()
    Peru = auto()
    Brasil = auto()
    Bolivia = auto()
    Paraguay = auto()
    Chile = auto()
    Argentina = auto()
    Uruguay = auto()

    def __lt__(self, other):
        if type(other) != type(self):
            return False

        return self.value < other.value

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        return self.value == other.value

    def __hash__(self):
        return hash(repr(self))


