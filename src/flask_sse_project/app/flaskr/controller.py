from flask import Blueprint, redirect
import random
from .bluetooth_controller import BluetoothController
from .gameFactory import GameFactory

import asyncio
import requests
#from asgiref.sync import sync_to_async
import concurrent.futures

class Controller(Blueprint):
    def __init__(self, name, import_Name, sse):
        Blueprint.__init__(self, name, import_Name)
        self.sse = sse
        self.startGame('badminton')
        redirect('/con/test')
        self.loop = asyncio.get_event_loop()
        #self.loop.run_until_complete(self.updateStream())
        #self.game.counterUp(1)
        #self.updateStream()
        self.bluetoothController = BluetoothController()
        #self.loop.run_until_complete(self.readBluetooth())

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

            requests.post('http://localhost:5000/con/test')
            #self.updateStream()

    def startGame(self, gameName):
        self.game = GameFactory.create(gameName)

    def updateStream(self):
        print('updateStream')
        gameState = self.game.gameState()
        self.sse.publish({'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2'],
                         'leftSide': random.randint(1,2), 'firstContact': 1, 'firstContactleft': 1}, type='updateData')
        #print(gameState['counter']['Team1'])
        #loop = asyncio.get_running_loop()
        #await loop.run_in_executor(None, self.sse.publish({'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2']}, type='updateData'))
        #with concurrent.futures.ProcessPoolExecutor() as pool:
            #loop.run_in_executor(pool, self.sse.publish({'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2']}, type='updateData'))
        #print('nach Publish')
        #restliche Werte hinzufügen

    def updateStream1(self): #zum testen des frontends
        gameState = self.game.gameState()
        self.sse.publish([{'status': 'game'},
          {'connectedController': 1},
          {'activeChooseField': 1},
          {'playMode': 1, 'activeChooseField1': 5, 'activeChooseField2': None},
          {'playMode': 1, 'activeChooseField1': 8, 'activeChooseField2': None},
          {'activeChooseField': 0},
          {'counterTeam1': 9, 'counterTeam2': 19}], type='updateData')