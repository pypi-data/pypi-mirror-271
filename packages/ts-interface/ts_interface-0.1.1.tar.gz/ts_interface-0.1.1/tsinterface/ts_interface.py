import abc


class TsInterface(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def load() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def predict(json_input: str) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def validate() -> str:
        pass


if __name__ == '__main__':
    ts = TsInterface()
    ts.load()
    ts.validate()
    output = ts.predict('test')
    print(output)
