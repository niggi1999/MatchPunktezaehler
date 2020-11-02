from flask import Blueprint

from .gameFactory import GameFactory

class Controller(Blueprint):
    def __init__(self, name, import_Name, sse):
        Blueprint.__init__(self, name, import_Name)
        self.sse = sse
        self.startGame('badminton')
        self.game.counterUp(2)

    def connectBluetooth(self):
        pass
        #subscriben zu device, das zurückkommt für countUp beide Teams und undo/redo

    def startGame(self, gameName):
        self.game = GameFactory.create(gameName)

    def updateStream(self):
        gameState = self.game.gameState()
        self.sse.publish({'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2']}, type='updateData')
        #restliche Werte hinzufügen