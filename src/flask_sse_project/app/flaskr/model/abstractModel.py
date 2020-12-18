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
        """
        Computes the press of the left button

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def up(self):
        """
        Computes the press of the up button

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def down(self):
        """
        Computes the press of the down button

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    async def ok(self):
        """
        Computes the press of the ok button

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def getCurrentSite(self):
        """
        Returns the current site

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def getPublishMethod(self):
        """
        Returns a Method which publishes to the SSE stream.

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def attach(self):
        """
        Attaches a new Observer

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def detach(self):
        """
        Detaches a Observer

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    async def _notifyUpdate(self):
        """
        Calls a Method in all Observers, which updates the displayed data

        Must be implemented in subclass.
        """
        pass