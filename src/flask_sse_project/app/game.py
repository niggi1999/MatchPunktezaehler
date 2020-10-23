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
        self.__undoStack = []
        self.__redoStack = []

    def counterUp(self, teamNumber):
        self.__undoStack.append(self.gameState())
        __redoStack = []

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

    def gameState(self):
        gameState = {"counter" : {"Team1" : self.counter["Team1"], "Team2" : self.counter["Team2"]},\
                     "wonRounds" : {"Team1" : self.wonRounds["Team1"], "Team2" : self.wonRounds["Team2"]},\
                     "wonGames" : {"Team1" : self.wonGames["Team1"], "Team2" : self.wonGames["Team2"]},\
                     "currentMaxPoints" : self.currentMaxPoints}
        return gameState

    def undo(self):
        if (0 == len(self.__undoStack)):
            raise ValueError
        else:
            self.__redoStack.append(self.gameState())

            lastGameState = self.__undoStack.pop()
            self.counter = lastGameState["counter"]
            self.wonRounds = lastGameState["wonRounds"]
            self.wonGames = lastGameState["wonGames"]
            self.currentMaxPoints = lastGameState["currentMaxPoints"]

    def redo(self):
        if (0 == len(self.__redoStack)):
            raise ValueError
        else:
            self.__undoStack.append(self.gameState())

            nextGameState = self.__redoStack.pop()
            self.counter = nextGameState["counter"]
            self.wonRounds = nextGameState["wonRounds"]
            self.wonGames = nextGameState["wonGames"]
            self.currentMaxPoints = nextGameState["currentMaxPoints"]