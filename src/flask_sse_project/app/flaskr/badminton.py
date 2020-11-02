#!/usr/bin/env python
from .game import Game

class Badminton(Game):
    maxPointsWithoutOvertime = 21
    absoluteMaxPoints = 30
    roundsInAGame = 2

    def isRoundOver(self):
        self.determineCurrentMaxPoints()
        if (self.currentMaxPoints == self.counter["Team1"] or self.currentMaxPoints == self.counter["Team2"]):
            self.currentMaxPoints = self.maxPointsWithoutOvertime
            return True
        else:
            return False

    def determineCurrentMaxPoints(self):
        isCounterEqual = self.counter["Team1"] == self.counter["Team2"]
        if (isCounterEqual and (self.counter["Team1"] >= 20)):
            self.currentMaxPoints = self.counter["Team1"] + 2
        if (self.currentMaxPoints >= self.absoluteMaxPoints):
            self.currentMaxPoints = self.absoluteMaxPoints

    def isGameOver(self):
        if (self.roundsInAGame == self.wonRounds["Team1"] or self.roundsInAGame == self.counter["Team2"]):
            return True
        else:
            return False