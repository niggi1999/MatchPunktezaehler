#!/usr/bin/env python
from abc import ABC, abstractmethod
from .abstractModel import AbstractModel

class Game(AbstractModel, ABC): #Must inherit in this order to be able to create a MRO
    """
    Abstract class that represents a game.

    When subclassed the class attributes and the methods isRoundOver() isGameOver() must be overridden.

    Class Attributes:

        maxPointsWithoutOvertime (int): The maximum number of points, when it doesn't come to an overtime.
        absoluteMaxPoints (int): The maximum number of points, when the overtime has its maximum duration.
        roundsInAGame (int): How many round must be won before the game is won.

    Attributes:

        counter (dict): Contains the current value of the counter.
        wonRounds (dict): Contains the number of won rounds by each team.
        wonGames (dict): Contains the number of won games by each team.
        currentMaxPoints (int): The maximum number of points till the round is over, if only one the
            would score.

    Methods:

        counterUp(): Increments the counter for the given team number.
        newRound(): Ends the current round and increments the wonRounds for the given team number.
        newGame(): Ends the current game and increments the wonGames for the given team.
        isRoundOver(): Checks if the current round is over.
        isGameOver(): Checks if the current game is over.
        gameState(): Returns the current game state.
        undo(): Undoes the last event.
        redo(): Redoes the last event.
    """
    maxPointsWithoutOvertime = 0
    absoluteMaxPoints = 0
    roundsInAGame = 0
    def __init__(self):
        """
        Initialises the objects attributes.
        """
        self.counter = {"Team1" : 0, "Team2" : 0}
        self.lastChanged = None
        self.wonRounds = {"Team1" : 0, "Team2" : 0}
        self.wonGames = {"Team1" : 0, "Team2" : 0}
        self.currentMaxPoints = self.maxPointsWithoutOvertime
        self.sidesChanged = False
        self.playerPositions = {"Team1" : {"Player1" : 1, "Player2": 2}, "Team2" : {"Player1" : 3, "Player2": 4}}
        self.servePosition = 0
        self._undoStack = []
        self._redoStack = []
        self.__observers = []
        self.updateModel()

    def right(self):
        self.counterUp(teamNumber = 2)

    def left(self):
        self.counterUp(teamNumber = 1)

    def up(self):
        try:
            self.redo()
        except ValueError as error:
            print(error)

    def down(self):
        try:
            self.undo()
        except ValueError as error:
            print(error)

    async def ok(self):
        await self.__notifyNewGame()

    def counterUp(self, teamNumber):
        """
        Increments the counter for the given team number.

        Updates the values of the undo and redo stack. Checks if the round is over and acts accordingly.

        Parameters:

            teamNumber (int): The team number for which the counter should be increased.

        Raises:

            ValueError: If the given team number is not valid.
        """
        self._undoStack.append(self.gameState())
        self._redoStack = []
        

        if (teamNumber not in range(1, 3)):
            raise ValueError('Team Number "{}" invalid'.format(teamNumber))
        winningTeam = "Team{}".format(teamNumber)
        self.counter[winningTeam] += 1
        self.lastChanged = winningTeam
        self.updateModel()
        if (self.isRoundOver()):
            self.newRound(teamNumber)

    def newRound(self, winningTeamNumber):
        """
        Ends the current round and increments the wonRounds for the given team number.

        Sets the counter of both teams to 0. Checks if with the end of the round the game is also over.

        Parameters:

            winningTeamNumber (int): The team number, which won the current round.
        """
        self.counter["Team1"] = 0
        self.counter["Team2"] = 0
        self.wonRounds["Team{}".format(winningTeamNumber)] += 1
        self.sidesChanged = not self.sidesChanged
        self.updateModel()
        if (self.isGameOver()):
            self.newGame(winningTeamNumber)

    def newGame(self, winningTeamNumber):
        """
        Ends the current game and increments the wonGames for the given team number.

        Sets the counter and won games of both teams to 0.

        Parameters:

            winningTeamNumber (int): The team number, which won the current game.
        """
        self.counter["Team1"] = 0
        self.counter["Team2"] = 0
        self.wonRounds["Team1"] = 0
        self.wonRounds["Team2"] = 0
        self.wonGames["Team{}".format(winningTeamNumber)] += 1
        self.updateModel

    @abstractmethod
    def isRoundOver(self):
        """
        Checks if the current round is over.

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def isGameOver(self):
        """
        Checks if the current game is over.

        Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def updateModel(self):
        """
        Updates information in Model

        Must be implemented in subclass
        """
        pass

    @abstractmethod
    def updateServePosition(self):
        """
        Gives the current serve Position

        Must be implemented in subclass.
        """
        pass

    def gameState(self):
        """
        Returns the current game state.

        Returns:

            gameState (dict): Contains the current counter, wonRound, wonGames and currentMaxPoints.
        """
        gameState = {"counter" : {"Team1" : self.counter["Team1"], "Team2" : self.counter["Team2"]},\
                     "lastChanged" : self.lastChanged,\
                     "wonRounds" : {"Team1" : self.wonRounds["Team1"], "Team2" : self.wonRounds["Team2"]},\
                     "wonGames" : {"Team1" : self.wonGames["Team1"], "Team2" : self.wonGames["Team2"]},\
                     "currentMaxPoints" : self.currentMaxPoints,\
                     "sidesChanged" : self.sidesChanged,\
                     "playerPositions" : self.playerPositions,\
                     "servePosition" : self.servePosition}
        return gameState

    def undo(self):
        """
        Undoes the last event.

        Raises:

            ValueError: If there are no events to undo.
        """
        if (0 == len(self._undoStack)):
            raise ValueError("Nothing to undo")
        else:
            self._redoStack.append(self.gameState())

            lastGameState = self._undoStack.pop()
            self.counter = lastGameState["counter"]
            self.wonRounds = lastGameState["wonRounds"]
            self.wonGames = lastGameState["wonGames"]
            self.currentMaxPoints = lastGameState["currentMaxPoints"]
            self.sidesChanged = lastGameState["sidesChanged"]
            self.playerPositions = lastGameState["playerPositions"]
            self.servePosition = lastGameState["servePosition"]

    def redo(self):
        """


        Raises:

            ValueError: If there are no events to redo.
        """
        if (0 == len(self._redoStack)):
            raise ValueError("Nothing to redo")
        else:
            self._undoStack.append(self.gameState())

            nextGameState = self._redoStack.pop()
            self.counter = nextGameState["counter"]
            self.wonRounds = nextGameState["wonRounds"]
            self.wonGames = nextGameState["wonGames"]
            self.currentMaxPoints = nextGameState["currentMaxPoints"]
            self.sidesChanged = nextGameState["sidesChanged"]
            self.playerPositions = nextGameState["playerPositions"]
            self.servePosition = nextGameState["servePosition"]

    def attach(self, observer):
        self.__observers.append(observer)

    def detach(self, observer):
        self.__observers.remove(observer)

    async def __notifyNewGame(self):
        for observer in self.__observers:
            await observer.changeModelToDialogLeaveGame()

    async def _notifyUpdate(self):
        for observer in self.__observers:
            await observer.updateSSE()


    def getCurrentSite(self):
        return "game"

    def getPublishMethod(self):
        return self.updateGameSite

    def updateGameSite(self, sse, bluetoothController):
        """
        Updates the SSE stream with the current counter.

        Must be called from Flask Request Context.
        """
        gameState = self.gameState()
        deviceCount = bluetoothController.deviceCount()
        sse.publish({"status": "game",
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
            "team1Left" : True,
            "opacityHighSiteTeam1" : 0.2,
            "opacityDownSiteTeam1" : 1,
            "opacityHighSiteTeam2" : 0.2,
            "opacityDownSiteTeam2" : 0.2}
            , type = "updateData")
        #asyncio.sleep(0.5)# TODO: Asynchron machen für aufblinken bei Punkt