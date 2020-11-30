from copy import deepcopy
from itertools import filterfalse

class TableModel():
    def __init__(self, site, configClass):
        self.__configClass = configClass
        self.__startCursor = self.__configClass.getStartCursor()
        self.newSite(site)

    def newSite(self, site) -> bool:
        setDimensionsWorked = self.__setDimensions(site)
        if setDimensionsWorked:
            self.__site = site
            self.cursor = deepcopy(self.__startCursor)
            self.selectedButtons = []
        return setDimensionsWorked

    def __setDimensions(self, site) -> bool:
        rowsAndColumns = self.__configClass.getRowsAndColumns(site)
        if rowsAndColumns:
            self.dimensions = {"rows" : rowsAndColumns["rows"], "columns" : rowsAndColumns["columns"]}
            return True
        return False

    def getCurrentSite(self):
        return deepcopy(self.__site)

    #TODO: In SiteModel verschieben
    '''
    def siteForward(self) -> bool:
        nextSite = self.__configClass.getNextSite(self.__site)
        if nextSite:
            self.newSite(nextSite)
            return True
        return False

    def siteBackward(self) -> bool:
        previousSite = self.__configClass.getPreviousSite(self.__site)
        if previousSite:
            self.newSite(previousSite)
            return True
        return False
    '''

    def goUp(self) -> bool:
        return self.__decrementCursor("vertically")

    def goDown(self) -> bool:
        return self.__incrementCursor("vertically")

    def goLeft(self) -> bool:
        return self.__decrementCursor("horizontally")

    def goRight(self) -> bool:
        return self.__incrementCursor("horizontally")

    def __decrementCursor(self, direction):
        rowOrColumn = self.__getAssociatedVector(direction)
        if self.cursor[rowOrColumn] > self.__startCursor[rowOrColumn]:
            self.cursor[rowOrColumn] -= 1
            return True
        else:
            return False

    def __incrementCursor(self, direction):
        rowOrColumn = self.__getAssociatedVector(direction)
        if self.cursor[rowOrColumn] < self.dimensions[rowOrColumn + "s"]:
            self.cursor[rowOrColumn] += 1
            return True
        else:
            return False

    @staticmethod
    def __getAssociatedVector(direction):
        rowOrColumn = None
        if "vertically" == direction:
            rowOrColumn = "row"
        elif "horizontally" == direction:
            rowOrColumn = "column"
        return rowOrColumn

    def selectCurrentButton(self):
        self.__deleteSelectedButtonOnSameRowOrColumnAsCursor()
        self.selectedButtons.append(deepcopy(self.cursor))
        print(self.selectedButtons)

    def __deleteSelectedButtonOnSameRowOrColumnAsCursor(self):
        elementInSameRowOrColumn = lambda element : (element["row"] == self.cursor["row"]) or\
                                                    (element["column"] == self.cursor["column"])
        self.selectedButtons[:] = filterfalse(elementInSameRowOrColumn, self.selectedButtons)
                            #[:] Notation to change elements of list and not
                            # change attribute to filterfalse object reference