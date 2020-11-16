#!/usr/bin/env python
from .game import Game

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