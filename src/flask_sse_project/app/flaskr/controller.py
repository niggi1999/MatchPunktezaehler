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
    """
    A class to connect the game to the Bluetooth input and send Updates to the frontend.

    Attributes
        sse (ServerSentEventsBlueprint): The Object for sending Server Sent Events.
        bluetoothController (BluetoothController): The BluetoothController, which returns the pressed buttons.
        bluetooth Tread (Thread): The Thread, which handles the output of the bluetoothController and
            updates the game and SSE stream.

    Methods
        setupBluetoothThread(): Configures a new Thread, which handles Bluetooth communication.
        readBluetooth(): Endless Loop in which a pressed button on the Bluetooth device
            updates the game and the SSE stream.
        startGame(): Starts the game.
        updateStream(): Updates the SSE stream (Must be called from Flask Request Context).
        updateSSE(): Sends a GET request to the given path to update the SSE stream.
        updateDeviceNumber(): Gets the number of connected devices and publishes it to the SSE stream.
    """
    def __init__(self, name, import_Name, sse):
        """
        Starts the game and initiates a daemon thread, which handles the bluetooth communication.

        Parameters:

            name (str): The name of the Blueprint.
            import_Name (str): The name of the blueprint package, usually ``__name__``.
                This helps locate the ``root_path`` for the blueprint.
            sse (ServerSentEventsBlueprint): The Object for sending Server Sent Events.

        """
        Blueprint.__init__(self, name, import_Name)
        self.sse = sse
        self.startGame('badminton')
        self.bluetoothTread = threading.Thread(target = self.setupBluetoothThread, daemon = True)
        self.bluetoothTread.start()

    def setupBluetoothThread(self):
        """
        Configures a new Thread, which handles Bluetooth communication.

        Should only be called from a new thread. After setup is complete, readBluetooth() will be called.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        with threading.Lock():
            self.bluetoothController = BluetoothController()
            self.bluetoothController.attach(self)
        loop.run_until_complete(self.readBluetooth())

    async def readBluetooth(self):
        """
        Endless Loop in which a pressed button on the Bluetooth device
        updates the game and the SSE stream

        Takes the pressed Button from the Bluetooth Controller and interprets it into the
        corresponding action for the game.
        Prints an error message if the requested action is not available in the game .
        Calls updateSSE() after updating the game.
        """
        while True:
            pressedButton = await self.bluetoothController.readBluetooth()
            if ('left' == pressedButton):
                self.game.counterUp(teamNumber = 1)
            elif ('right' == pressedButton):
                self.game.counterUp(teamNumber = 2)
            elif ('down' == pressedButton):
                try:
                    self.game.undo()
                except ValueError as error:
                    print(error)
            elif ('up' == pressedButton):
                try:
                    self.game.redo()
                except ValueError as error:
                    print(error)
            else:
                continue

            await self.updateSSE("updateCounter")

    async def updateSSE(self, path):
        """
        Sends a GET request to the given path to update the SSE stream.

        Parameters:

            path (str): The path to which the request will be sent.
                Without the prefix "http://localhost:5000/con/"
        """
        async with httpx.AsyncClient() as client:
            r = await client.get("http://localhost:5000/con/" + path)
            print(r.text)


    def updateDeviceCount(self):
        """
        Gets the number of connected devices and publishes it to the SSE stream.
        """
        deviceCount = self.bluetoothController.deviceCount()
        self.sse.publish({'deviceCount': deviceCount}, type='updateDeviceCount')


    def startGame(self, gameName):
        """
        Starts the game.

        Calls the GameFactory to create a new game.

        Parametes:

            gameName (str): The name of the game to be started.
        """
        self.game = GameFactory.create(gameName)

    def updateStream(self):
        """
        Updates the SSE stream (Must be called from Flask Request Context).
        """
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