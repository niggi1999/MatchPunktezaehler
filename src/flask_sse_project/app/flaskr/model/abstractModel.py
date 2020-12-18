from abc import ABC, abstractmethod

class AbstractModel(ABC):
    """
    Abstract Base Class for all Models

    When subclassed all methods must be implemented.
    """
    @abstractmethod
    def right(self):
        """
        Computes the press of the right button

        Must be implemented in subclass.
        """
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
    async def ok(self):
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