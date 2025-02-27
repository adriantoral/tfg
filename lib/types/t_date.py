from datetime import datetime

from lib.interfaces.types import ITypes


class TDate(ITypes):
    def __init__(self, value: str | datetime):
        self._value = f"#{value if isinstance(value, str) else value.now().strftime('%Y-%m-%d %H:%M:%S')}#"

    def __repr__(self):
        return self._value
