from flask import Blueprint
import random
from .bluetooth_controller import BluetoothController
from .gameFactory import GameFactory

import asyncio

class Controller(Blueprint):
    def __init__(self, name, import_Name, sse):
        Blueprint.__init__(self, name, import_Name)
        self.sse = sse
        self.startGame('badminton')
        self.bluetoothController = BluetoothController()
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.readBluetooth())

    async def readBluetooth(self):
        while True:
            pressedButton = await self.bluetoothController.readAsync()
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


    def startGame(self, gameName):
        self.game = GameFactory.create(gameName)

    def updateStream(self):
        gameState = self.game.gameState()
        self.sse.publish({'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2'],
                         'leftSide': random.randint(1,2), 'firstContact': random.randint(1,2), 'firstContactleft': random.randint(0,1)}, type='updateData')
        #restliche Werte hinzufügen