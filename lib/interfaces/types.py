from abc import abstractmethod


class ITypes:
    @abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return self.__repr__()
