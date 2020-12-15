#!/usr/bin/env python
from .game import Game
from enum import IntEnum
from random import randint

class ServePosition(IntEnum):
    """
    Enum Class that represents the servePosition
    """
    TEAM1LEFT = 1
    TEAM1RIGHT = 2
    TEAM2LEFT = 3
    TEAM2RIGHT = 4
    UNKNOWN = 0

class Badminton(Game):
    """
    Class that represents the game badminton.

    Subclass of game.

    Class Attibutes:

        maxPointsWithoutOvertime (int): The maximum number of points, when it doesn't come to an overtime.
            Overrides the parent class implementation.
        absoluteMaxPoints (int): The maximum number of points, when the overtime has its maximum duration.
            Overrides the parent class implementation.
        roundsInAGame (int): How many round must be won before the game is won.
            Overrides the parent class implementation.

    Methods:

        isRoundOver(): Checks if the current round is over.
        determineCurrentMaxPoints(): Checks if the game is in overtime and determines
            the current max points accordingly.
        isGameOver(): Checks if the current game is over.
    """
    maxPointsWithoutOvertime = 21
    absoluteMaxPoints = 30
    roundsInAGame = 2

    def isRoundOver(self):
        """
        Checks if the current round is over.

        Calls determineCurrentMaxPoints() to update currentMaxPoints. When the round is over
        resets currentMaxPoints to maxPointsWithoutOvertime.

        Returns:

            True: If the current round is over.
            False: If the current round is not over.
        """
        self.determineCurrentMaxPoints()
        if (self.currentMaxPoints == self.counter["Team1"] or self.currentMaxPoints == self.counter["Team2"]):
            self.currentMaxPoints = self.maxPointsWithoutOvertime
            return True
        else:
            return False

    def determineCurrentMaxPoints(self):
        """
        Checks if the game is in overtime and determines the current max points accordingly.

        Checks if the counters are equal at 20:20 or higher. If that is true, currentMaxPoints will be set to
        the value of one counter + 2. currentMaxPoints will never exceed absoluteMaxPoints.

        Example:

            If the counter is 20:20, currentMaxPoints will be set to 22.
            If the counter rises to 21:20, currentMaxPoints will stay at 22.
            Only if both teams score one after the other, currentMaxPoints will be incremented.
            So at 21:21, currentMaxPoints will be 23.
        """
        isCounterEqual = self.counter["Team1"] == self.counter["Team2"]
        if (isCounterEqual and (self.counter["Team1"] >= (self.maxPointsWithoutOvertime - 1))):
            self.currentMaxPoints = self.counter["Team1"] + 2
        if (self.currentMaxPoints >= self.absoluteMaxPoints):
            self.currentMaxPoints = self.absoluteMaxPoints

    def isGameOver(self):
        """
        Checks if the current game is over.

        Returns:

            True: If the current game is over.
            False: If the current game is not over.
        """
        if (self.roundsInAGame == self.wonRounds["Team1"] or self.roundsInAGame == self.counter["Team2"]):
            return True
        else:
            return False
    
    def updateModel(self):
        self.updateServePosition()
        self.updatePlayerPositions()

    def updateServePosition(self):
        """
        Updates and gives the current serve Position

        Returns:

            ServePosition Enum
        """
        if (ServePosition.UNKNOWN == self.servePosition or 0 == len(self._undoStack)):
            randomNumber = randint(1,2)
            if(randomNumber == 1): 
                self.servePosition = ServePosition.TEAM1RIGHT
                return ServePosition.TEAM1RIGHT
            elif(randomNumber == 2): 
                self.servePosition = ServePosition.TEAM2RIGHT
                return ServePosition.TEAM2RIGHT
            else: 
                self.servePosition = ServePosition.UNKNOWN
                return ServePosition.UNKNOWN
        else:
            
            lastGameState = self._undoStack[-1]
            lastCounter = lastGameState["counter"]

            isEven = lambda x : ((x % 2) == 0)

            if(self.counter["Team1"] > lastCounter["Team1"]):
                if(isEven(self.counter["Team1"])):
                    self.servePosition = ServePosition.TEAM1RIGHT
                    return ServePosition.TEAM1RIGHT
                else:
                    self.servePosition = ServePosition.TEAM1LEFT
                    return ServePosition.TEAM1LEFT
                    
            if(self.counter["Team2"] > lastCounter["Team2"]):
                if(isEven(self.counter["Team2"])):
                    self.servePosition = ServePosition.TEAM2RIGHT
                    return ServePosition.TEAM2RIGHT
                else:
                    self.servePosition = ServePosition.TEAM2LEFT
                    return ServePosition.TEAM2LEFT

        self.servePosition = ServePosition.UNKNOWN
        return ServePosition.UNKNOWN

    def updatePlayerPositions(self):
        """
        Updates the current player positions
        
        The player positions inside the playfield are represented by integers.
        The meaning of these numbers are as follows:

           |Monitor|
         _____________
        |      |      |
        |  1   |  4   |
        |______|______|
        |      |      |
        |  2   |  3   |
        |______|______|
        """
        self.updatePlayerPositionsSideChanged()
        self.updatePlayerPositionsServeAndScore()
        return
    
    def updatePlayerPositionsSideChanged(self):
        """
        Updates the player position when sides are switched.
        """
        currentPlayerPositoins = self.playerPositions
        newPlayerPositions = {}

        if(False == self.sidesChanged):
            if(1 == currentPlayerPositoins["Team1"]["Player1"] or 2 == currentPlayerPositoins["Team1"]["Player1"]):
                newPlayerPositions = currentPlayerPositoins
            else:
                newPlayerPositions = {"Team1" : {"Player1" : currentPlayerPositoins["Team1"]["Player1"] - 2,\
                                                 "Player2" : currentPlayerPositoins["Team1"]["Player2"] - 2},\
                                      "Team2" : {"Player1" : currentPlayerPositoins["Team2"]["Player1"] + 2,\
                                                 "Player2" : currentPlayerPositoins["Team2"]["Player2"] + 2}
                                     }
        else:
            if(3 == currentPlayerPositoins["Team1"]["Player1"] or 4 == currentPlayerPositoins["Team1"]["Player1"]):
                newPlayerPositions = currentPlayerPositoins
            else:
                newPlayerPositions = {"Team1" : {"Player1" : currentPlayerPositoins["Team1"]["Player1"] + 2,\
                                                 "Player2" : currentPlayerPositoins["Team1"]["Player2"] + 2},\
                                      "Team2" : {"Player1" : currentPlayerPositoins["Team2"]["Player1"] - 2,\
                                                 "Player2" : currentPlayerPositoins["Team2"]["Player2"] - 2}
                                     }
        
        self.playerPositions = newPlayerPositions
        return

    def updatePlayerPositionsServeAndScore(self):
        """
        Updates player positions when the serving team scores a point.
        """
        return
    