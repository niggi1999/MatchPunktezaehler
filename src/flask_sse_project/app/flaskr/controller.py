from flask import Blueprint
from .bluetooth_controller import BluetoothController
from .model import SiteModel, AbstractModel, GameFactory, SiteProdConfig

import asyncio
import threading
import httpx

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
        self.sse = sse #TODO: In SseConroller verschieben
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
        loop.run_until_complete(self.changeModelToFirstSite())
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

            await self.updateSSE("updateSite") #TODO: Nur zum Test, später nur aus SseController heraus, SseController zum Observer von siteModel machen

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
        if "init" == self.model.getCurrentSite():
            await self.updateSSE("updateSite")

    async def changeModelToGame(self):
        self.model.detach(self)
        gameName = self.model.getGameName()
        playerColors = self.model.getPlayerColors()
        self.model = GameFactory.create(gameName, playerColors)
        self.model.attach(self)

    async def changeModelToFirstSite(self):
        self.model.detach(self)
        self.model = SiteModel(SiteProdConfig)
        self.model.attach(self)

    async def changeModelToLeaveGameDialog(self): #TODO: implementieren
        pass

    def startGame(self, gameName):
        """
        Starts the game.

        Calls the GameFactory to create a new game.

        Parametes:

            gameName (str): The name of the game to be started.
        """
        self.game = GameFactory.create(gameName)

    def updateSite(self):
        publishMethod = self.model.getPublishMethod()
        publishMethod(self.sse, self.bluetoothController)