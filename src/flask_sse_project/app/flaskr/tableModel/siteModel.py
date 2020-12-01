from .tableFactory import TableFactory
from .config import SiteProdConfig

from copy import deepcopy

class SiteModel():
    def __init__(self, siteConfig = SiteProdConfig, testSite = None):
        self.__config = siteConfig
        self.__firstSite = self.__config.getFirstSite()
        if testSite:
            self.__site = testSite
        else:
            self.__site = deepcopy(self.__firstSite)
        self.__tableModel = TableFactory.create(self.__site, self.__config)
        self.__startElementNewSite = self.__config.getStartElementNewSite()
        self.__firstSiteStartElement = self.__config.getFirstSiteStartElement()
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

    def getSelectedButtonCurrentSiteVerbose(self):
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
        getNewElement = self.__getSiteMethodAssociatedToHorizontalDirection(direction)
        nextSiteElement = getNewElement(currentElement = self.__activeSiteElement,\
                                                   attributeName = "siteElements")
        if nextSiteElement:
            self.__activeSiteElement = nextSiteElement
            return True
        else:
            return False

    def __getSiteMethodAssociatedToHorizontalDirection(self, direction) -> callable:#Durch getattr ersetzen
        if "right" == direction:
            return self.__config.getNextElement
        elif "left" == direction:
            return self.__config.getPreviousElement

    def __getTableMethodAssociatedToHorizontalDirection(self, direction) -> callable:#Durch getattr ersetzen
        if "right" == direction:
            return self.__tableModel.goRight
        elif "left" == direction:
            return self.__tableModel.goLeft

    def ok(self):
        if "table" == self.__activeSiteElement:
            self.__tableModel.selectCurrentButton()
        elif "nextButton" == self.__activeSiteElement:
            self.__siteForward()
        elif "previousButton" == self.__activeSiteElement:
            self.__siteBackward()

    def __siteForward(self) -> bool:
        return self.__newSite("forward")

    def __siteBackward(self) -> bool:
        return self.__newSite("backward")

    def __newSite(self, direction) -> bool:
        #if in eigene Methode
        methodName = ""
        if "backward" == direction:
            methodName = "getPreviousElement"
        elif "forward" == direction:
            methodName = "getNextElement"
        else:
            raise ValueError
        newSite = getattr(self.__config, methodName)(self.__site, "succession")
        if newSite:
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
    def firstSite(self):
    def notify(self):
        #Wenn Übergang zu game
    '''