from flask import Blueprint
import random #nur Test
from .bluetooth_controller import BluetoothController
from .gameFactory import GameFactory

import asyncio
import threading
import httpx
#from asgiref.sync import sync_to_async
#import concurrent.futures

class Controller(Blueprint):
    def __init__(self, name, import_Name, sse):
        Blueprint.__init__(self, name, import_Name)
        self.sse = sse
        self.startGame('badminton')
        self.bluetoothTread = threading.Thread(target = self.setupBluetoothThread, daemon = True)
        self.bluetoothTread.start()

    def setupBluetoothThread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        with threading.Lock():
            self.bluetoothController = BluetoothController()
        loop.run_until_complete(self.readBluetooth())


    async def readBluetooth(self):
        while True:
            pressedButton = await self.bluetoothController.readBluetooth()
            print(pressedButton)
            if ('left' == pressedButton):
                self.game.counterUp(1)
            elif ('right' == pressedButton):
                self.game.counterUp(2)
            elif ('down' == pressedButton):
                try:
                    self.game.undo()
                except ValueError:
                    print('Nothing to undo')
            elif ('up' == pressedButton):
                try:
                    self.game.redo()
                except ValueError:
                    print('Nothing to redo')
            else:
                continue

            async with httpx.AsyncClient() as client:
                r = await client.get("http://localhost:5000/con/updateCounter")
                print(r.text)

    def startGame(self, gameName):
        self.game = GameFactory.create(gameName)

    def updateStream(self):
        print('updateStream')
        gameState = self.game.gameState()
        self.sse.publish({'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2'],
                         'leftSide': random.randint(1,2), 'firstContact': 1, 'firstContactleft': 1}, type='updateData')

    def updateStream1(self): #zum testen des frontends
        gameState = self.game.gameState()
        self.sse.publish([{'status': 'game'},
          {'connectedController': 1},
          {'activeChooseField': 1},
          {'playMode': 1, 'activeChooseField1': 5, 'activeChooseField2': None},
          {'playMode': 1, 'activeChooseField1': 8, 'activeChooseField2': None},
          {'activeChooseField': 0},
          {'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2']}], type='updateData')