from .tableFactory import TableFactory
from .config import SiteProdConfig

from copy import deepcopy
import asyncio

class SiteModel():
    def __init__(self, siteConfig = SiteProdConfig, testSite = None):
        self.__config = siteConfig
        self.__firstSite = self.__config.getFirstSite()
        if testSite is None:
            self.__site = deepcopy(self.__firstSite)
        else:
            self.__site = testSite
        self.__tableModel = TableFactory.create(self.__site, self.__config)
        self.__startElementNewSite = self.__config.getStartElementNewSite()
        self.__firstSiteStartElement = self.__config.getFirstSiteStartElement()
        self.__observers = []
        self.__loop = asyncio.get_event_loop()
        self.__setActiveElementNewSite()
        self.__buildSelectedButtonsStore()

    def __buildSelectedButtonsStore(self):
        self.selectedButtonsStore = {}
        nextSite = self.__firstSite
        while nextSite:
            self.selectedButtonsStore[nextSite] = []
            nextSite = self.__config.getNextElement(nextSite, "succession")

    def __getSelectedButtonCurrentSite(self):
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
        select()

    def __siteForward(self) -> bool:
        print("SiteForward")
        #TODO: test if Elements are Selected
        return self.__newSite("forward")

    def __siteBackward(self) -> bool:
        print("SiteBackward")
        return self.__newSite("backward")

    def __newSite(self, direction) -> bool:
        newSite = self.__getConfigMethodAssociatedToHorizontalDirection(direction)(self.__site, "succession")
        if newSite is not None:
            self.selectedButtonsStore[self.__site] = self.__getSelectedButtonCurrentSite()
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

    '''
    async def notify(self):
        for observer in self.__observers:
            observer.changeToGame()
    '''

    #def __firstSite(self):