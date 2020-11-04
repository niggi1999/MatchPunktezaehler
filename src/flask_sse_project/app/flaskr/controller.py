from flask import Blueprint

from .bluetoothController import BluetoothController
from .gameFactory import GameFactory

class Controller(Blueprint):
    def __init__(self, name, import_Name, sse):
        Blueprint.__init__(self, name, import_Name)
        self.sse = sse
        self.startGame('badminton')
        self.bluetoothController = BluetoothController()
        self.readBluetooth()

    def readBluetooth(self):
        while True:
            pressedButton = self.bluetoothController.readLoop()
            if ('counter1' == pressedButton):
                self.game.counterUp(1)
            elif ('counter2' == pressedButton):
                self.game.counterUp(2)
            elif ('undo' == pressedButton):
                try:
                    self.game.undo()
                except ValueError:
                    print('Nothing to undo')
            elif ('redo' == pressedButton):
                try:
                    self.game.redo()
                except ValueError:
                    print('Nothing to redo')
            else:
                continue

            self.updateStream()
        #subscriben zu device, das zurückkommt für countUp beide Teams und undo/redo

    def startGame(self, gameName):
        self.game = GameFactory.create(gameName)

    def updateStream(self):
        gameState = self.game.gameState()
        self.sse.publish({'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2']}, type='updateData')
        #restliche Werte hinzufügen