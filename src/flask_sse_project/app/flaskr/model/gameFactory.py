#!/usr/bin/env python
from .badminton import Badminton

import inspect
class GameFactory():
    """ Factory class to create a game Object. """
    @staticmethod
    def create(specificGameName, playerColors = None):
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
            stack = inspect.stack()
            caller = stack[1][0].f_locals["self"].__class__.__name__
            if playerColors is None and "controller" == caller:
                raise ValueError("No Player Colors")
            return Badminton(playerColors)
        else:
            raise ValueError('Game name: "{}" invalid'.format(specificGameName))