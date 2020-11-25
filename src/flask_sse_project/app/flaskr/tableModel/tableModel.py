from copy import deepcopy
from itertools import filterfalse

class TableModel():
    def __init__(self, configClass, testSite = None):
        self.configClass = configClass
        if None == testSite:
            testSite = self.configClass.getFirstSite()
        self.__newSite(testSite)

    def __newSite(self, site, gameForm = "singles"):
        self.site = site
        self.__setDimensions(site, gameForm)
        self.__startCursor = self.configClass.getStartCursor()
        self.cursor = deepcopy(self.__startCursor)
        self.selectedButtons = []

    def __setDimensions(self, site, gameForm):
        rowsAndColumns = self.configClass.getRowsAndColumns(self.site)
        self.dimensions = {"rows" : rowsAndColumns["rows"], "columns" : rowsAndColumns["columns"]}
        if ("colorMenu" == site) and ("doubles" == gameForm):
            playersPerTeam = 2
            self.dimensions["columns"] = self.dimensions["columns"] * playersPerTeam

    def goUp(self) -> bool:
        return self.__decrementCursor("vertically")

    def goDown(self) -> bool:
        return self.__incrementCursor("vertically")

    def goLeft(self) -> bool:
        return self.__decrementCursor("horizontally")

    def goRight(self) -> bool:
        return self.__incrementCursor("horizontally")

    def __decrementCursor(self, direction):
        rowOrColumn = self.__getAssociatedString(direction)
        if self.cursor[rowOrColumn] > self.__startCursor[rowOrColumn]:
            self.cursor[rowOrColumn] -= 1
            return True
        else:
            return False

    def __incrementCursor(self, direction):
        rowOrColumn = self.__getAssociatedString(direction)
        if self.cursor[rowOrColumn] < self.dimensions[rowOrColumn + "s"]:
            self.cursor[rowOrColumn] += 1
            return True
        else:
            return False

    def __getAssociatedString(self, direction):
        rowOrColumn = None
        if "vertically" == direction:
            rowOrColumn = "row"
        elif "horizontally" == direction:
            rowOrColumn = "column"
        return rowOrColumn

    def selectCurrentButton(self) -> bool:
        self.__deleteSelectedOnSameRowOrColumnAsCursor()
        self.selectedButtons.append(deepcopy(self.cursor))
        print(self.selectedButtons)
        return True

    def __deleteSelectedOnSameRowOrColumnAsCursor(self):
        elementInSameRowOrColumn = lambda element : (element["row"] == self.cursor["row"]) or\
                                                    (element["column"] == self.cursor["column"])
        self.selectedButtons[:] = filterfalse(elementInSameRowOrColumn, self.selectedButtons)
                            #[:] Notation to change elements of list and not
                            # change attribute to filterfalse object reference

    #def nextSite(self):