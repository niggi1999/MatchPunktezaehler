#!/usr/bin/env python
from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self):
        self.counterTeam1 = 0
        self.counterTeam2 = 0
        self.wonRoundsTeam1 = 0
        self.wonRoundsTeam2 = 0
        self.maxPoints = 21    #TODO: auf 0, in Unterklasse richtiger Wert

    def counterUp(self, teamNumber):
        if (teamNumber not in range(1, 3)):
            raise ValueError('Team Number "{}" invalid'.format(teamNumber))
        if (1 == teamNumber):
            self.counterTeam1 += 1
        if (2 == teamNumber):
            self.counterTeam2 += 1
        if (self.isRoundOver()):
            self.counterTeam1 = 0
            self.counterTeam2 = 0
            if (1 == teamNumber):
                self.wonRoundsTeam1 += 1
            if (2 == teamNumber):
                self.wonRoundsTeam2 += 1

    @abstractmethod
    def isRoundOver(self):
        pass


#if (__name__ == '__main__'):
