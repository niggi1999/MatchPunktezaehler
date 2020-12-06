from abc import ABC, abstractmethod

class AbstractModel(ABC):
    @abstractmethod
    def right(self):
        pass
    @abstractmethod
    def left(self):
        pass
    @abstractmethod
    def up(self):
        pass
    @abstractmethod
    def down(self):
        pass
    @abstractmethod
    def ok(self):
        pass