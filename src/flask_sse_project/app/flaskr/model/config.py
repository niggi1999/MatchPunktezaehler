from better_abc import ABCMeta, abstract_attribute

from copy import deepcopy

class TableConfig(metaclass=ABCMeta):
    _succession = abstract_attribute()
    _requiredButtonsCount = abstract_attribute()
    _rowsInit = abstract_attribute()
    _columnsInit = abstract_attribute()
    _rowsPlayerMenu = abstract_attribute()
    _columnsPlayerMenu = abstract_attribute()
    _rowsColorMenu = abstract_attribute()
    _columnsColorMenuSingles = abstract_attribute()
    _columnsColorMenuDoubles = abstract_attribute()
    _rowsGameMenu = abstract_attribute()
    _columnsGameMenu = abstract_attribute()
    _startCursor = abstract_attribute()
    _rowsAndColumns = abstract_attribute()

    @classmethod
    def getNextElement(cls, currentElement, attributeName):
        attribute = getattr(cls, "_" + attributeName)
        nextSite = None
        for index, item in enumerate(attribute):
            if item == currentElement:
                try:
                    nextSite = attribute[index + 1]
                except IndexError:
                    pass
                break
        return nextSite

    @classmethod
    def getPreviousElement(cls, currentElement, attributeName):
        attribute = getattr(cls, "_" + attributeName)
        previousSite = None
        for index, item in enumerate(attribute):
            if item == currentElement:
                if 0 != index:
                    previousSite = attribute[index - 1]
                break
        return previousSite

    @classmethod
    def getRowsAndColumns(cls, currentSite):
        for key, value in cls._rowsAndColumns.items():
            if key == currentSite:
                return deepcopy(value)

    @classmethod
    def getFirstSite(cls):
        return cls._succession[0]

    @classmethod
    def getStartCursor(cls):
        return deepcopy(cls._startCursor)

    @classmethod
    def getRequiredButtonsCount(cls, site):
        return deepcopy(cls._requiredButtonsCount[site])

class TableTestConfig(TableConfig):
    _succession = ("init", "playerMenu", "colorMenu", "gameMenu")
    _requiredButtonsCount = {"init" : 0, "playerMenu" : 1, "colorMenuSingles" : 2, "colorMenuDoubles" : 4, "gameMenu" : 1}
    _rowsInit = ("deviceCountTEST",)
    _columnsInit = ("deviceCount",)
    _rowsPlayerMenu = ("mode",)
    _columnsPlayerMenu = ("singles", "doubles")
    _rowsColorMenu = ("orange", "red", "purple", "blue", "green", "black")
    _columnsColorMenuSingles = ("team1", "team2")
    _columnsColorMenuDoubles = ("player1", "player2", "player3", "player4")
    _rowsGameMenu = ("badminton",)
    _columnsGameMenu = ("game",)
    _rowsDialog = ("button",)
    _columnsDialog = ("cancel", "ok")
    _startCursor = {"row" : 1, "column" : 1}
    _rowsAndColumns = {
        "init" : {"rows" : 1, "columns" : 1,\
                  "rowContents" : _rowsInit, "columnContents" : _columnsInit},
        "playerMenu" : {"rows" : 1, "columns" : 2,\
                        "rowContents" : _rowsPlayerMenu, "columnContents" : _columnsPlayerMenu},
        "colorMenuSingles" : {"rows" : 6, "columns" : 2,\
                       "rowContents" : _rowsColorMenu, "columnContents" : _columnsColorMenuSingles},
        "colorMenuDoubles" : {"rows" : 6, "columns" : 4,
                              "rowContents" : _rowsColorMenu, "columnContents" : _columnsColorMenuDoubles},
        "gameMenu" : {"rows" : 1, "columns" : 1,\
                      "rowContents" : _rowsGameMenu, "columnContents" : _columnsGameMenu},
        "dialog" : {"rows" : 1, "columns" : 2,\
                           "rowContents" : _rowsDialog, "columnContents" : _columnsDialog}
    }

class TableProdConfig(TableConfig):
    _succession = ("init", "playerMenu", "colorMenu", "gameMenu")
    _requiredButtonsCount = {"init" : 0, "playerMenu" : 1, "colorMenuSingles" : 2, "colorMenuDoubles" : 4, "gameMenu" : 1}
    _rowsInit = ("deviceCount",)
    _columnsInit = ("deviceCount",)
    _rowsPlayerMenu = ("mode",)
    _columnsPlayerMenu = ("singles", "doubles")
    _rowsColorMenu = ("orange", "red", "purple", "blue", "green", "black")
    _columnsColorMenuSingles = ("team1", "team2")
    _columnsColorMenuDoubles = ("player1", "player2", "player3", "player4")
    _rowsGameMenu = ("badminton",)
    _columnsGameMenu = ("game",)
    _rowsDialog = ("button",)
    _columnsDialog = ("cancel", "ok")
    _startCursor = {"row" : 1, "column" : 1}
    _rowsAndColumns = {
        "init" : {"rows" : 1, "columns" : 1,\
                  "rowContents" : _rowsInit, "columnContents" : _columnsInit},
        "playerMenu" : {"rows" : 1, "columns" : 2,\
                        "rowContents" : _rowsPlayerMenu, "columnContents" : _columnsPlayerMenu},
        "colorMenuSingles" : {"rows" : 6, "columns" : 2,\
                       "rowContents" : _rowsColorMenu, "columnContents" : _columnsColorMenuSingles},
        "colorMenuDoubles" : {"rows" : 6, "columns" : 4,
                              "rowContents" : _rowsColorMenu, "columnContents" : _columnsColorMenuDoubles},
        "gameMenu" : {"rows" : 1, "columns" : 1,\
                      "rowContents" : _rowsGameMenu, "columnContents" : _columnsGameMenu},
        "dialog" : {"rows" : 1, "columns" : 2,\
                           "rowContents" : _rowsDialog, "columnContents" : _columnsDialog}
    }

class SiteConfig(metaclass=ABCMeta):
    _siteElements = abstract_attribute()
    _firstSiteStartElement = abstract_attribute()
    _startElementNewSite = abstract_attribute()

    @classmethod
    def getFirstSiteStartElement(cls):
        return deepcopy(cls._firstSiteStartElement)

    @classmethod
    def getStartElementNewSite(cls):
        return deepcopy(cls._startElementNewSite)

    @classmethod
    def setAttribute(cls, attributeName, value):
        '''
        Only for testing
        '''
        setattr(cls, attributeName, value)

    @classmethod
    def getAttribute(cls, attributeName):
        '''
        Only for testing
        '''
        return deepcopy(getattr(cls, attributeName))

class SiteTestConfig(SiteConfig, TableTestConfig):
    _siteElements = ("previousButton", "table", "nextButton")
    _firstSiteStartElement = "nextButton"
    _startElementNewSite = "table"

class SiteProdConfig(SiteConfig, TableProdConfig):
    _siteElements = ("previousButton", "table", "nextButton")
    _firstSiteStartElement = "nextButton"
    _startElementNewSite = "table"