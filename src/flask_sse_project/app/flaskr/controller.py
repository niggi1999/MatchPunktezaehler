from flask import Blueprint
from .bluetooth_controller import BluetoothController
from .gameFactory import GameFactory
from .siteModel import SiteModel

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
        self.sse = sse
        #self.startGame('badminton') #badminton als default behalten
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
            #TODO: Folgendes in Methode unterbringen
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

            await self.updateSSE("updateGameSite")

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

    async def updateDeviceCount(self):
        pass
        #if "init" == self.tableModel.site: #TODO: tableModel muss erstellt werden
            #self.updateSSE("updateInit")

    def startGame(self, gameName):
        """
        Starts the game.

        Calls the GameFactory to create a new game.

        Parametes:

            gameName (str): The name of the game to be started.
        """
        self.game = GameFactory.create(gameName)

    def updateInitSite(self):
        deviceCount = self.bluetoothController.deviceCount()
        self.sse.publish({"status": "init",
        "cursorElement" : "forwardButton",
        "connectedController": deviceCount},
        type = "updateData")

    def updatePlayerMenuSite(self):
        #activeChooseField = {}.get(self.siteModel.getSelectedButtonsCurrentSiteVerbose())
        self.sse.publish({"status": "playerMenu",
        "cursorElement" : "forwardButton",
        "activeChooseField": 1,
        "fieldNames" : None},
        type = "updateData")

    def updateColorMenuSite(self):
        self.sse.publish({"status": "nameMenu",
        "cursorElement" : "forwardButton",
        "playMode": 1,
        "color1Team1": 3, "color2Team1": None,
        "color1Team2": 5, "color2Team2": None,
        "fieldNames" : ["Orange", "Red", "Purple", "Blue", "Green", "Black"],
        "tableActive" : 2},
        type = "updateData")

    def updateGameMenuSite(self):
        self.sse.publish({"status": "gameMenu",
        "cursorElement" : "forwardButton",
        "activeChooseField": "badminton",
        "fieldNames" : ["Badminton", "Volleyball", "Tennis"]},
        type = "updateData")

    def updateGameSite(self):
        """
        Updates the SSE stream with the current counter.

        Must be called from Flask Request Context.
        """
        gameState = self.game.gameState()
        deviceCount = self.bluetoothController.deviceCount()
        self.sse.publish({"status": "game",
            "connectedController" : deviceCount,
            "counterTeam1": gameState["counter"]["Team1"],
            "counterTeam2": gameState["counter"]["Team2"],
            "lastChanged" : gameState["lastChanged"],
            "roundsTeam1" : gameState["wonRounds"]["Team1"],
            "roundsTeam2" : gameState["wonRounds"]["Team2"],
            "gamesTeam1": gameState["wonGames"]["Team1"],
            "gamesTeam2": gameState["wonGames"]["Team2"],
            "team1HighColor" : 'Green',
            "team1DownColor" : 'Orange',
            "team2HighColor" : 'Blue',
            "team2DownColor" : 'Red',
            "team1Left" : False,
            "opacityHighSiteTeam1" : 0.2,
            "opacityDownSiteTeam1" : 1,
            "opacityHighSiteTeam2" : 0.2,
            "opacityDownSiteTeam2" : 0.2}
            , type = "updateData")