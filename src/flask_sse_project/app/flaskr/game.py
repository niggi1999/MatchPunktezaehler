#!/usr/bin/env python
from abc import ABC, abstractmethod

class Game(ABC):
    """
    Abstract class that represents a game.

    When subclassed the class attributes and the methods isRoundOver() isGameOver() must be overridden.

    Class Attibutes:

        maxPointsWithoutOvertime (int): The maximum number of points, when it doesn't come to an overtime.
        absoluteMaxPoints (int): The maximum number of points, when the overtime has its maximum duration.
        roundsInAGame (int): How many round must be won before the game is won.

    Attributes:

        counter (dict): Contains the current value of the counter.
        wonRounds (dict): Contains the number of won rounds by each team.
        wonGames (dict): Contains the number of won games by each team.
        currentMaxPoints (int): The maximum number of points till the round is over, if only one the
            would score.

    Methods:

        counterUp(): Increments the counter for the given team number.
        newRound(): Ends the current round and increments the wonRounds for the given team number.
        newGame(): Ends the current game and increments the wonGames for the given team.
        isRoundOver(): Checks if the current round is over.
        isGameOver(): Checks if the current game is over.
        gameState(): Returns the current game state.
        undo(): Undoes the last event.
        redo(): Redoes the last event.
    """
    maxPointsWithoutOvertime = 0
    absoluteMaxPoints = 0
    roundsInAGame = 0
    def __init__(self):
        """
        Initialises the objects attributes.
        """
        self.counter = {"Team1" : 0, "Team2" : 0}
        self.wonRounds = {"Team1" : 0, "Team2" : 0}
        self.wonGames = {"Team1" : 0, "Team2" : 0}
        self.currentMaxPoints = self.maxPointsWithoutOvertime
        self._undoStack = []
        self.__redoStack = []

    def counterUp(self, teamNumber):
        """
        Increments the counter for the given team number.

        Updates the values of the undo and redo stack. Checks if the round is over and acts accordingly.

        Parameters:

            teamNumber (int): The team number for which the counter should be increased.

        Raises:

            ValueError: If the given team number is not valid.
        """
        self._undoStack.append(self.gameState())
        self.__redoStack = []

        if (teamNumber not in range(1, 3)):
            raise ValueError('Team Number "{}" invalid'.format(teamNumber))
        self.counter["Team{}".format(teamNumber)] += 1
        if (self.isRoundOver()):
            self.newRound(teamNumber)

    def newRound(self, winningTeamNumber):
        """
        Ends the current round and increments the wonRounds for the given team number.

        Sets the counter of both teams to 0. Checks if with the end of the round the game is also over.

        Parameters:

            winningTeamNumber (int): The team number, which won the current round.
        """
        self.counter["Team1"] = 0
        self.counter["Team2"] = 0
        self.wonRounds["Team{}".format(winningTeamNumber)] += 1
        if (self.isGameOver()):
            self.newGame(winningTeamNumber)

    def newGame(self, winningTeamNumber):
        """
        Ends the current game and increments the wonGames for the given team number.

        Sets the counter and won games of both teams to 0.

        Parameters:

            winningTeamNumber (int): The team number, which won the current game.
        """
        self.counter["Team1"] = 0
        self.counter["Team2"] = 0
        self.wonRounds["Team1"] = 0
        self.wonRounds["Team2"] = 0
        self.wonGames["Team{}".format(winningTeamNumber)] += 1

    @abstractmethod
    def isRoundOver(self):
        """
        Checks if the current round is over.

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def isGameOver(self):
        """
        Checks if the current game is over.

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def servePosition(self):
        """
        Gives the current serve Position

        Must be implemented in subclass.
        """
        pass

    def gameState(self):
        """
        Returns the current game state.

        Returns:

            gameState (dict): Contains the current counter, wonRound, wonGames and currentMaxPoints.
        """
        gameState = {"counter" : {"Team1" : self.counter["Team1"], "Team2" : self.counter["Team2"]},\
                     "wonRounds" : {"Team1" : self.wonRounds["Team1"], "Team2" : self.wonRounds["Team2"]},\
                     "wonGames" : {"Team1" : self.wonGames["Team1"], "Team2" : self.wonGames["Team2"]},\
                     "currentMaxPoints" : self.currentMaxPoints}
        return gameState

    def undo(self):
        """
        Undoes the last event.

        Raises:

            ValueError: If there are no events to undo.
        """
        if (0 == len(self._undoStack)):
            raise ValueError("Nothing to undo")
        else:
            self.__redoStack.append(self.gameState())

            lastGameState = self._undoStack.pop()
            self.counter = lastGameState["counter"]
            self.wonRounds = lastGameState["wonRounds"]
            self.wonGames = lastGameState["wonGames"]
            self.currentMaxPoints = lastGameState["currentMaxPoints"]

    def redo(self):
        """
        Redoes the last event.

        Raises:

            ValueError: If there are no events to redo.
        """
        if (0 == len(self.__redoStack)):
            raise ValueError("Nothing to redo")
        else:
            self._undoStack.append(self.gameState())

            nextGameState = self.__redoStack.pop()
            self.counter = nextGameState["counter"]
            self.wonRounds = nextGameState["wonRounds"]
            self.wonGames = nextGameState["wonGames"]
            self.currentMaxPoints = nextGameState["currentMaxPoints"]