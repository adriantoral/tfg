from lib.interfaces.types import ITypes


class TNull(ITypes):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return 'NULL'
