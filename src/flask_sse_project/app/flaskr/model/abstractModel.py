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

    @abstractmethod
    def getCurrentSite(self):
        pass

    @abstractmethod
    def getPublishMethod(self):
        pass

    @abstractmethod
    def attach(self):
        pass

    @abstractmethod
    def detach(self):
        pass

    @abstractmethod
    async def _notifyUpdate(self):
        pass