#!/usr/bin/env python
from .badminton import Badminton
class GameFactory():
    """ Factory class to create a game Object. """
    @classmethod
    def create(cls, specificGameName):
        """
        Creates a new game Object.

        Parameters:

            secificGameName (str): The name of the game, that should be created

        Returns:

            A object of a subclass of Game corresponding to the given specificGameName

        Raises:

            ValueError: If the gives specificGameName is not corresponding to any subclass of game
        """
        if ("badminton" == specificGameName):
            return Badminton()
        else:
            raise ValueError('Game name: "{}" invalid'.format(specificGameName))