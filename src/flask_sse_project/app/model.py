#!/usr/bin/env python
from gameFactory import GameFactory

class Model():
    def startGame(self, gameName):
        self.game = GameFactory.create(gameName)
        #TODO:Anzeige ändern