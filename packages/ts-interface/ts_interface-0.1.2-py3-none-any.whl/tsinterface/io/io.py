import abc


class IO(abc.ABC):

    @abc.abstractmethod
    def to_dict(self):
        pass
