from better_abc import ABCMeta, abstract_attribute

from copy import deepcopy

class TableConfig(ABCMeta):
    _succession = abstract_attribute()
    _columnsPlayerMenu = abstract_attribute()
    _rowsColorMenu = abstract_attribute()
    _rowsAndColumns = abstract_attribute()
    _startCursor = abstract_attribute()

    @classmethod
    def getNextSite(cls, currentSite):
        nextSite = None
        for index, item in enumerate(cls._succession):
            if item == currentSite:
                try:
                    nextSite = cls._succession[index + 1]
                except IndexError:
                    pass
                break
        return nextSite

    @classmethod
    def getPreviousSite(cls, currentSite):
        previousSite = None
        for index, item in enumerate(cls._succession):
            if item == currentSite:
                if 0 != index:
                    previousSite = cls._succession[index - 1]
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

class TableTestConfig(TableConfig):
    _succession = ("init", "playerMenu", "colorMenu", "gameMenu", "game")
    _columnsPlayerMenu = ("singles", "doubles")
    _rowsColorMenu = ("Orange", "Red", "Purple", "Blue", "Green", "Black")
    _startCursor = {"row" : 1, "column" : 1}
    _rowsAndColumns = {
        "init" : {"rows" : 1, "columns" : 1},
        "playerMenu" : {"rows" : 1, "columns" : 2, "columnContents" : _columnsPlayerMenu},
        "colorMenu" : {"rows" : 6, "columns" : 2, "rowContents" : _rowsColorMenu},
        "gameMenu" : {"rows" : 1, "columns" : 1}
    }

class TableProdConfig(TableConfig):
    _succession = ("init", "playerMenu", "colorMenu", "gameMenu", "game")
    _columnsPlayerMenu = ("singles", "doubles")
    _rowsColorMenu = ("Orange", "Red", "Purple", "Blue", "Green", "Black")
    _startCursor = {"row" : 1, "column" : 1}
    _rowsAndColumns = {
        "init" : {"rows" : 1, "columns" : 1},
        "playerMenu" : {"rows" : 1, "columns" : 2, "columnContents" : _columnsPlayerMenu},
        "colorMenu" : {"rows" : 6, "columns" : 2, "rowContents" : _rowsColorMenu},
        "gameMenu" : {"rows" : 1, "columns" : 1}
    }