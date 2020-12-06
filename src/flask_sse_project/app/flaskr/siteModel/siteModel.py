from .tableFactory import TableFactory
from .config import SiteProdConfig
from .model import AbstractModel

from copy import deepcopy
import asyncio

class SiteModel(AbstractModel):
    def __init__(self, siteConfig = SiteProdConfig, testSite = None):
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

    def ok(self):
        select = {
            "table" : self.__tableModel.selectCurrentButton,
            "nextButton" : self.__siteForward,
            "previousButton" : self.__siteBackward
        }.get(self.__activeSiteElement)
        try:
            select()
        except (TypeError, ValueError) as error:
            print(error)

    def __siteForward(self):
        print("SiteForward")
        if self.__requiredButtonsOnSiteAreSelected():
            nextSiteExists = self.__newSite("forward")
            if not nextSiteExists:
                self.__loop.run_until_complete(self.__notify())
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
        currentSite = self.__site
        isInColorMenu = "colorMenuSingles" == self.__site or "colorMenuDoubles" == self.__site
        if isInColorMenu:
            currentSite = "colorMenu"
        newSite = self.__getConfigMethodAssociatedToHorizontalDirection(direction)(currentSite, "succession")
        if newSite is not None: # TODO: Methode für color Menu ifs
            self.selectedButtonsStore[self.__site] = self.__getSelectedButtonsCurrentSite()
            if "colorMenu" == newSite:
                modeButtonCoordinates = self.selectedButtonsStore["playerMenu"][0]
                mode = self.__tableModel.getButtonName(modeButtonCoordinates, "playerMenu")
                if "singlesmode" == mode:
                    newSite = "colorMenuSingles"
                elif "doublesmode" == mode:
                    newSite = "colorMenuDoubles"
            self.__tableModel.newTable(newSite, self.selectedButtonsStore[newSite])
            self.__site = newSite
            self.__setActiveElementNewSite
            return True
        return False

    def __setActiveElementNewSite(self):
        if self.__firstSite == self.__site:
            self.__activeSiteElement = self.__firstSiteStartElement
        else:
            self.__activeSiteElement = self.__startElementNewSite

    def attach(self, observer):
        self.__observers.append(observer)

    def detach(self, observer):
        self.__observers.remove(observer)

    async def __notify(self):
        for observer in self.__observers:
            await observer.changeModelToGame()

    #def __firstSite(self):