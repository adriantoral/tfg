from lib.interfaces.types import ITypes


class TInteger(ITypes):
    def __init__(self, value):
        self.value = str(value)

    def __repr__(self):
        return self.value
