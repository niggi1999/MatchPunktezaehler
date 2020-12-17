from .tableFactory import TableFactory
from .abstractModel import AbstractModel

from typing import Callable
class DialogModel(AbstractModel):
    def __init__(self, site):
        self.__site = site
        self.__tableModel = TableFactory.create("dialog")
        self.__observers = []

    def right(self):
        if self.__tableModel.goRight():
            self._notifyUpdate()

    def left(self):
        if self.__tableModel.goLeft():
            self._notifyUpdate()

    def up(self):
        pass

    def down(self):
        pass

    def getCurrentSite(self):
        return self.__site

    async def ok(self):
        buttonName = self.getCursorButtonName()
        if "ok" == buttonName:
            self._notifyOk()
        elif "cancel" == buttonName:
            self._notifyCancel()

    def getCursor(self):
        return self.__tableModel.getCursorVerbose()

    def getCursorButtonName(self):
        cursor = self.getCursor()
        cursorSse = cursor.split()[0]
        return cursorSse

    def getCursorForSse(self):
        buttonName = self.getCursorButtonName()
        cursorSse = ""
        if "ok" == buttonName:
            cursorSse = "forwardButton"
        elif "cancel" == buttonName:
            cursorSse = "backwardButton"
        return cursorSse

    def attach(self, observer):
        self.__observers.append(observer)

    def detach(self, observer):
        self.__observers.remove(observer)

    async def _notifyUpdate(self):
        for observer in self.__observers:
            await observer.updateSSE()

    def _notifyOk(self):
        if "newGameDialog" == self.__site:
            for observer in self.__observers:
                observer.changeModelToFirstSite()
        elif "changeSidesDialog" == self.__site:
            for observer in self.__observers:
                observer.changeModelToGame()

    def _notifyCancel(self):
        for observer in self.__observers:
            observer.changeModelToGame()

    def getPublishMethod(self) -> Callable:
        siteCapitalized = self.__site[0].upper() + self.__site[1:]
        publishMethod = getattr(self, "update" + siteCapitalized)
        return publishMethod

    def updateNewGameDialog(self, sse, bluetoothController):
        del bluetoothController
        sse.publish({"status": "leaveGame",
            "cursorElement" : self.getCursorForSse()})

    def updateSideChangeDialog(self, sse, bluetoothController):
        del bluetoothController
        sse.publish({"status": "changeSides",
            "cursorElement" : self.getCursorForSse()})