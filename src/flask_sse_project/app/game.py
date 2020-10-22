#!/usr/bin/env python
from abc import ABC, abstractmethod

class Game(ABC):
    maxPointsWithoutOvertime = 0
    absoluteMaxPoints = 0
    roundsInAGame = 0
    def __init__(self):
        self.counter = {"Team1" : 0, "Team2" : 0}
        self.wonRounds = {"Team1" : 0, "Team2" : 0}
        self.wonGames = {"Team1" : 0, "Team2" : 0}
        self.currentMaxPoints = self.maxPointsWithoutOvertime

    def counterUp(self, teamNumber):
        if (teamNumber not in range(1, 3)):
            raise ValueError('Team Number "{}" invalid'.format(teamNumber))
        self.counter["Team{}".format(teamNumber)] += 1
        if (self.isRoundOver()):
            self.newRound(teamNumber)

    def newRound(self, winningTeamNumber):
        self.counter["Team1"] = 0
        self.counter["Team2"] = 0
        self.wonRounds["Team{}".format(winningTeamNumber)] += 1
        if (self.isGameOver()):
            self.newGame(winningTeamNumber)

    def newGame(self, winningTeamNumber):
        self.counter["Team1"] = 0
        self.counter["Team2"] = 0
        self.wonRounds["Team1"] = 0
        self.wonRounds["Team2"] = 0
        self.wonGames["Team{}".format(winningTeamNumber)] += 1

    @abstractmethod
    def isRoundOver(self):
        pass

    @abstractmethod
    def isGameOver(self):
        pass