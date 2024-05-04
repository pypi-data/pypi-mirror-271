from abc import abstractmethod, ABC


class ActionArgumentParser(ABC):
    def __call__(self, name):
        self.create(name)

    @abstractmethod
    def create(self, name):
        raise RuntimeError("Not implemented")
