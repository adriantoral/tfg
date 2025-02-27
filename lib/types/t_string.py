from lib.interfaces.types import ITypes


class TString(ITypes):
    def __init__(self, value: str):
        self._value = f"'{value}'"

    def __repr__(self):
        return self._value
