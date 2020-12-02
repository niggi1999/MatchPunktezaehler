from copy import deepcopy
from itertools import filterfalse

class TableModel():
    def __init__(self, site, configClass):
        self.__configClass = configClass
        self.__startCursor = self.__configClass.getStartCursor()
        self.newTable(site)

    def newTable(self, site, selectedButtons = []) -> bool:
        setDimensionsWorked = self.__setDimensions(site)
        if setDimensionsWorked:
            self.__site = site
            self.cursor = deepcopy(self.__startCursor)
            self.selectedButtons = selectedButtons
        return setDimensionsWorked

    def __setDimensions(self, site) -> bool:
        rowsAndColumns = self.__configClass.getRowsAndColumns(site)
        if rowsAndColumns is not None:
            self.dimensions = {"rows" : rowsAndColumns["rows"], "columns" : rowsAndColumns["columns"]}
            self.__rowContents = rowsAndColumns["rowContents"]
            self.__columnContents = rowsAndColumns["columnContents"]
            return True
        return False

    def getCurrentSite(self):
        return deepcopy(self.__site)

    def getCursorVerbose(self) -> str:
        rowContent = self.__getContent("row", self.cursor)
        columnContent = self.__getContent("column", self.cursor)
        return (columnContent + rowContent)

    def getSelectedButtonsVerbose(self) -> str:
        selectedButtonsVerbose = []
        for button in self.selectedButtons:
            rowContent = self.__getContent("row", button)
            columnContent = self.__getContent("column", button)
            selectedButtonsVerbose.append(columnContent + rowContent)
        return selectedButtonsVerbose

    def __getContent(self, rowOrColumn, tableCoordinatesDict):
        contents = getattr(self, "_TableModel__" + rowOrColumn + "Contents")
        content = contents[tableCoordinatesDict[rowOrColumn] - 1]
        return content

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
        return {
            "vertically" : "row",
            "horizontally" : "column"
        }.get(direction)

    def selectCurrentButton(self):
        print("Select Current Button")
        self.__deleteSelectedButtonOnSameRowOrColumnAsCursor()
        self.selectedButtons.append(deepcopy(self.cursor))

    def __deleteSelectedButtonOnSameRowOrColumnAsCursor(self):
        elementInSameRowOrColumn = lambda element : (element["row"] == self.cursor["row"]) or\
                                                    (element["column"] == self.cursor["column"])
        self.selectedButtons[:] = filterfalse(elementInSameRowOrColumn, self.selectedButtons)
                            #[:] Notation to change elements of list and not
                            # change attribute to filterfalse object reference