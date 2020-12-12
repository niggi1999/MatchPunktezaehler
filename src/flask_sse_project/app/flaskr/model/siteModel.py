from .tableFactory import TableFactory
from .abstractModel import AbstractModel

from copy import deepcopy
from typing import Dict
import asyncio

class SiteModel(AbstractModel):
    def __init__(self, siteConfig, testSite = None):
        self.__config = siteConfig
        self.__setInitialValues()
        self.__setInitialSite(testSite)
        self.__setActiveElementNewSite()
        self.__buildSelectedButtonsStore()
        self.__tableModel = TableFactory.create(self.__site, self.__config)

    def __setInitialSite(self, testSite):
        if testSite is None:
            self.__site = deepcopy(self.__firstSite)
        else:
            self.__site = testSite

    def __setInitialValues(self):
        self.__firstSite = self.__config.getFirstSite()
        self.__startElementNewSite = self.__config.getStartElementNewSite()
        self.__firstSiteStartElement = self.__config.getFirstSiteStartElement()
        self.__observers = []
        self.__loop = asyncio.get_event_loop()

    def __buildSelectedButtonsStore(self):
        self.selectedButtonsStore = {}
        nextSite = self.__firstSite
        while nextSite is not None:
            if "colorMenu" == nextSite:
                self.selectedButtonsStore["colorMenuSingles"] = []
                self.selectedButtonsStore["colorMenuDoubles"] = []
                nextSite = self.__config.getNextElement("colorMenu", "succession")
            else:
                self.selectedButtonsStore[nextSite] = []
                nextSite = self.__config.getNextElement(nextSite, "succession")

    def __getSelectedButtonsCurrentSite(self):
        return deepcopy(self.__tableModel.selectedButtons)

    def getSelectedButtonsCurrentSiteVerbose(self):
        return deepcopy(self.__tableModel.getSelectedButtonsVerbose())

    def getActiveElement(self) -> str:
        activeElement = self.__activeSiteElement
        if "table" == activeElement:
            activeElement = self.__tableModel.getCursorVerbose()
        return activeElement

    def up(self) -> bool:
        if "table" == self.__activeSiteElement:
            return self.__tableModel.goUp()
        else:
            return False

    def down(self) -> bool:
        if "table" == self.__activeSiteElement:
            return self.__tableModel.goDown()
        else:
            return False

    def left(self) -> bool:
        moveWorked = self.__moveHorizontal("left")
        if self.__site == self.__firstSite:
            self.right()
            moveWorked = False
        return moveWorked

    def right(self) -> bool:
        return self.__moveHorizontal("right")

    def __moveHorizontal(self, direction) -> bool:
        if "table" == self.__activeSiteElement:
            moveInDirection = self.__getTableMethodAssociatedToHorizontalDirection(direction)
            moveWorked = moveInDirection()
            if moveWorked:
                return True
        getNewElement = self.__getConfigMethodAssociatedToHorizontalDirection(direction)
        nextSiteElement = getNewElement(currentElement = self.__activeSiteElement,\
                                                   attributeName = "siteElements")
        if nextSiteElement is not None:
            self.__activeSiteElement = nextSiteElement
            return True
        else:
            return False

    def __getConfigMethodAssociatedToHorizontalDirection(self, direction) -> callable:
        next = dict.fromkeys(["right", "forward"], self.__config.getNextElement)
        previous = dict.fromkeys(["left", "backward"], self.__config.getPreviousElement)
        return {**next, **previous}.get(direction)      # **Operator unpacks Dict (Used to merge dicts)

    def __getTableMethodAssociatedToHorizontalDirection(self, direction) -> callable:
        return {
            "right" : self.__tableModel.goRight,
            "left" : self.__tableModel.goLeft
        }.get(direction)

    async def ok(self):
        select = {
            "table" : self.__tableModel.selectCurrentButton,
            "nextButton" : self.__siteForward,
            "previousButton" : self.__siteBackward
        }.get(self.__activeSiteElement)
        try:
            await select()
        except (TypeError, ValueError) as error:
            print(error)

    async def __siteForward(self):
        print("SiteForward")
        if self.__requiredButtonsOnSiteAreSelected():
            nextSiteExists = self.__newSite("forward")
            if not nextSiteExists:
                await self.__notifyStartGame()
        else:
            raise ValueError("More selected Buttons are required to move forward")

    def __requiredButtonsOnSiteAreSelected(self) -> bool:
        requiredButtonsCount = self.__config.getRequiredButtonsCount(self.__site)
        actualButtonsCount = len(self.__tableModel.selectedButtons)
        return requiredButtonsCount == actualButtonsCount

    def __siteBackward(self):
        print("SiteBackward")
        previousSiteExists = self.__newSite("backward")
        if not previousSiteExists:
            raise TypeError("No previous Site")

    def __newSite(self, direction) -> bool:
        currentSite = self.getCurrentSite()
        newSite = self.__getConfigMethodAssociatedToHorizontalDirection(direction)(currentSite, "succession")
        if newSite is not None:
            self.selectedButtonsStore[self.__site] = self.__getSelectedButtonsCurrentSite()
            if "colorMenu" == newSite:
                newSite = self.__getParticularSiteForColorMenu()
            self.__tableModel.newTable(newSite, self.selectedButtonsStore[newSite])
            self.__site = newSite
            self.__setActiveElementNewSite()
            return True
        return False

    def getCurrentSite(self):
        currentSite = self.__site
        isInColorMenu = "colorMenuSingles" == self.__site or "colorMenuDoubles" == self.__site
        if isInColorMenu:
            currentSite = "colorMenu"
        return currentSite

    def __getParticularSiteForColorMenu(self):
        modeButtonCoordinates = self.selectedButtonsStore["playerMenu"][0]
        mode = self.__tableModel.getButtonName(modeButtonCoordinates, "playerMenu")
        site = ""
        if "singlesmode" == mode:
            site = "colorMenuSingles"
        elif "doublesmode" == mode:
            site = "colorMenuDoubles"
        return site

    def __setActiveElementNewSite(self):
        if self.__firstSite == self.__site:
            self.__activeSiteElement = self.__firstSiteStartElement
        else:
            self.__activeSiteElement = self.__startElementNewSite

    def attach(self, observer):
        self.__observers.append(observer)

    def detach(self, observer):
        self.__observers.remove(observer)

    async def __notifyStartGame(self): #TODO: Umbenennen
        for observer in self.__observers:
            await observer.changeModelToGame()

    #TODO: Zweites notify für update Data
    async def _notifyUpdate(self):
        for observer in self.__observers:
            await observer.updateSSE()

    #Methode die updated Zurückgeben, Methode bekommt sse und bluetooth Controller übergeben
    #TODO: Alles weiter unten refaktorieren
    def getPublishMethod(self):
        siteCapitalized = self.__site[0].upper() + self.__site[1:]
        publishMethod = getattr(self, "update" + siteCapitalized + "Site")
        return publishMethod

    def updateInitSite(self, sse, bluetoothController):
        deviceCount = bluetoothController.deviceCount()
        sse.publish({"status": "init",
        "cursorElement" : self.getActiveElement(),
        "connectedController": deviceCount},
        type = "updateData")

    def updatePlayerMenuSite(self, sse, bluetoothController):
        del bluetoothController
        selectedButtons = self.getSelectedButtonsCurrentSiteVerbose()
        activeChooseField = selectedButtons[0]["column"] if selectedButtons else None
        activeElement = self.getActiveElement()
        cursorElement = activeElement.split()[0]
        columnContents = self.__tableModel.getColumnContents()
        sse.publish({"status": "playerMenu",
        "cursorElement" : cursorElement,
        "activeChooseField": activeChooseField,
        "fieldNames" : columnContents},
        type = "updateData")

    def updateColorMenuSinglesSite(self, sse, bluetoothController):
        playModeInteger = 1
        self.updateColorMenuSite(sse, bluetoothController, playModeInteger)

    def updateColorMenuDoublesSite(self, sse, bluetoothController):
        playModeInteger = 2
        self.updateColorMenuSite(sse, bluetoothController, playModeInteger)

    def updateColorMenuSite(self, sse, bluetoothController, playModeInteger):
        del bluetoothController
        teamColors = self.__getTeamColors()
        activeElement = self.getActiveElement()
        print("ACTIVEELEMENT")
        print(activeElement)
        activeElementHasMoreThanOneWord = 1 < len(activeElement.split())
        print("ACTIVEELEMENTHASMORETHANONEWORD")
        print(activeElementHasMoreThanOneWord)
        columnActiveElement = activeElement.split()[1] if activeElementHasMoreThanOneWord else activeElement
        rowActiveElement = activeElement.split()[0] if activeElementHasMoreThanOneWord else activeElement
        print("TABLEACTIVEVORHER")
        print(rowActiveElement)
        if "nextButton" == rowActiveElement:
            rowActiveElement = 1 * playModeInteger
        elif "previousButton" == rowActiveElement:
            rowActiveElement = 2 * playModeInteger
        else:
            rowActiveElement = rowActiveElement[-1]
        print("COLOR1TEAM1")
        print(teamColors["color1Team1"])
        print("TABLEACTIVE")
        print(rowActiveElement)
        sse.publish({"status": "nameMenu",
        "cursorElement" : rowActiveElement,
        "playMode": playModeInteger,
        "fieldNames" : self.__tableModel.getRowContents(),
        "color1Team1": teamColors["color1Team1"], "color2Team1": teamColors["color2Team1"],
        "color1Team2": teamColors["color1Team2"], "color2Team2": teamColors["color2Team2"],
        "tableActive" : columnActiveElement},
        type = "updateData")

    def __getTeamColors(self) -> Dict[str, str]:
        color1Team1 = color2Team1 = color1Team2 = color2Team2 = None
        selectedButtons = self.getSelectedButtonsCurrentSiteVerbose()
        for button in selectedButtons:
            columnName = button["column"]
            if "Team1" == columnName:
                color1Team1 = color2Team1 = button["row"]
            elif "Team2" == columnName:
                color1Team2 = color2Team2 = button["row"]
            elif "Player1" == columnName:
                color1Team1 = button["row"]
            elif "Player2" == columnName:
                color2Team1 = button["row"]
            elif "Player3" == columnName:
                color1Team2 = button["row"]
            elif "Player4" == columnName:
                color2Team2 = button["row"]
        teamColors = {"color1Team1" : color1Team1, "color2Team1" : color2Team1,\
                      "color1Team2" : color1Team2, "color2Team2" : color2Team2}
        return teamColors

    def updateGameMenuSite(self, sse, bluetoothController):
        del bluetoothController
        activeElement = self.getActiveElement()
        activeElementHasMoreThanOneWord = 1 < len(activeElement.split())
        rowActiveElement = activeElement.split()[0] if activeElementHasMoreThanOneWord else activeElement
        selectedButtons = self.getSelectedButtonsCurrentSiteVerbose()
        activeChooseField = selectedButtons[0]["column"] if selectedButtons else None
        sse.publish({"status": "gameMenu",
        "cursorElement" : rowActiveElement,
        "activeChooseField": activeChooseField,
        "fieldNames" : self.__tableModel.getRowContents()},
        type = "updateData")