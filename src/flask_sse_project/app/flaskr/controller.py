from flask import Blueprint
from .bluetoothController import BluetoothController
from .model import SiteModel, AbstractModel, GameFactory, SiteProdConfig, DialogModel

import httpx

import asyncio
import threading
from copy import deepcopy


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
    def __init__(self, name, import_Name, sse, bluetoothController):
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
        self.model = None
        self.lastGameState = None
        self.bluetoothTread = threading.Thread(target = self.setupBluetoothThread,\
                                               args = (bluetoothController,), daemon = True)
        self.bluetoothTread.start()

    def setupBluetoothThread(self, bluetoothController):
        """
        Configures a new Thread, which handles Bluetooth communication.

        Should only be called from a new thread. After setup is complete, readBluetooth() will be called.
        Not Thread Safe
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        #with threading.Lock():
        self.changeModelToFirstSite()
        self.bluetoothController = bluetoothController
        self.bluetoothController.attach(self)
        #self.siteModel = SiteModel()
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
            if ("left" == pressedButton):
                self.model.left()
            elif ("right" == pressedButton):
                self.model.right()
            elif ("down" == pressedButton):
                self.model.down()
            elif ("up" == pressedButton):
                self.model.up()
            elif ("ok" == pressedButton):
                await self.model.ok()
            else:
                continue

            await self.updateSSE("updateSite")

    @staticmethod
    async def updateSSE(path):
        """
        Sends a GET request to the given path to update the SSE stream.

        Parameters:

            path (str): The path to which the request will be sent.
                Without the prefix "http://localhost:5000/con/"
        """
        async with httpx.AsyncClient() as client:
            r = await client.get("http://localhost:5000/con/" + path)
            print(r.text)
            print("")

    async def updateDeviceCount(self):
        """
        Updates the shown device count
        """
        if "init" == self.model.getCurrentSite():
            await self.updateSSE("updateSite")

    def changeModelToGame(self, changeSidesRequested = False):
        """
        Changes the Model to a specific game
        """
        self.model.detach(self)
        if self.lastGameState is None:
            gameName = self.model.getGameName()
            playerColors = self.model.getPlayerColors()
            self.model = GameFactory.create(gameName, playerColors)
        else:
            self.model = GameFactory.create(self.lastGameState["gameName"])
            self.model.setGameState(self.lastGameState)
            self.lastGameState = None
        if changeSidesRequested:
            self.model.changeSides()

        self.model.attach(self)

    def changeModelToFirstSite(self):
        """
        Resets the model to the first site
        """
        self.lastGameState = None
        if self.model is not None:
            self.model.detach(self)
        self.model = SiteModel(SiteProdConfig)
        self.model.attach(self)

    def changeModelToLeaveGameDialog(self):
        """
        Changes the Model to a leave game dialog

        Saves the current Game State, so it can be resumed
        """
        self.lastGameState = self.model.gameState()
        self.model = DialogModel("newGameDialog")
        self.model.attach(self)

    def changeModelToChangeSidesDialog(self):
        """
        Changes the Model to a change sides dialog

        Saves the current Game State, so it can be resumed
        """
        self.lastGameState = self.model.gameState()
        self.model = DialogModel("changeSidesDialog")
        self.model.attach(self)

    def updateSite(self):
        """
        Updates the displayed data
        """
        publishMethod = self.model.getPublishMethod()
        publishMethod(self.sse, self.bluetoothController)