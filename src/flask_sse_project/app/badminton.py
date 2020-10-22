#!/usr/bin/env python
from game import Game

class Badminton(Game):
    def isRoundOver(self):
        isCounterEqual = self.counterTeam1 == self.counterTeam2
        if (isCounterEqual and (self.counterTeam1 >= 20)):
            self.maxPoints = self.counterTeam1 + 2

        if (self.maxPoints == self.counterTeam1 or self.maxPoints == self.counterTeam2):
            self.maxPoints = 21
            return True
        else:
            return False
