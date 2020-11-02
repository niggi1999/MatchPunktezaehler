import random

from flask import Blueprint

from .gameFactory import GameFactory

class Controller(Blueprint):
    def __init__(self, name, import_Name, sse):
        Blueprint.__init__(self, name, import_Name)
        self.sse = sse

    def startGame(self, gameName):
        self.game = GameFactory.create(gameName)
        #TODO:Anzeige ändern

    def updateStream(self):
        self.sse.publish({'counterTeam1': random.randrange(1, 100), 'counterTeam2': random.randrange(1, 100)}, type='updateData')