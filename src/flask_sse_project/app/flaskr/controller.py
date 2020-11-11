from flask import Blueprint, redirect
import random
from .bluetooth_controller import BluetoothController
from .gameFactory import GameFactory

import asyncio
import requests
import httpx
import threading
import _thread
import os
import sys
#from asgiref.sync import sync_to_async
import concurrent.futures

class Controller(Blueprint):
    def __init__(self, name, import_Name, sse):
        Blueprint.__init__(self, name, import_Name)
        self.sse = sse
        self.startGame('badminton')
        #redirect('/con/test')
        #self.loop = asyncio.get_event_loop()
        #self.loop.run_until_complete(self.updateStream())
        #self.game.counterUp(1)
        #self.updateStream()
        #self.bluetoothController = BluetoothController()
        #self.loop.run_until_complete(self.readBluetooth())
        #bluetoothTread = threading.Thread(target = self.readBluetooth)
        #bluetoothTread.deamon = True
        #bluetoothTread.run()
        _thread.start_new_thread(self.readBluetooth)  #Deamon
        print("hinter Thread")

    '''
    def readBluetoothTest(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.readBluetooth())
    '''

    def readBluetooth(self):
        #with threading.Lock():
        #Lock
        self.bluetoothController = BluetoothController()
        try:
            while True:
                #print("readBluetooth")
                pressedButton = self.bluetoothController.readLoop()
                print(pressedButton)
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

                print("über GET")
                #os.system("curl http://127.0.0.1:5000/con/test")
                test = requests.get("http://127.0.0.1:5000/con/test")
                print(test.text)
                #print(test.url)
                #print(test.text)
                #async with httpx.AsyncClient() as client:
                    #r = await client.get("http://localhost:5000/con/test")
                print("unter GET")
                #self.updateStream()
        except KeyboardInterrupt:
            sys.exit(1)

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
          {'counterTeam1': gameState['counter']['Team1'], 'counterTeam2': gameState['counter']['Team2']}], type='updateData')