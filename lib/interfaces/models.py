from abc import abstractmethod

from lib.tables.table import Table
from lib.utils.build_query import build_query_colums


class IModels:
    @staticmethod
    @abstractmethod
    def create(*args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def read(*args, **kwargs):
        pass

    def _save(
            self,
            where,
            read_value,
            model: 'IModels',
            table: Table,
            ignore: list[str],
            is_update: bool = False
    ):
        data = build_query_colums(self.__dict__, ignore)

        if is_update:
            table.update(**data, where=where)
            return

        table.insert(**data)
        self.__dict__.update(model.read(read_value).pop().__dict__)

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass
