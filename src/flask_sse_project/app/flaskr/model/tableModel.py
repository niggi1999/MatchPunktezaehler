from copy import deepcopy
from itertools import filterfalse
from typing import List, Dict, Type

from .config import TableConfig

class TableModel():
    def __init__(self, site, config: Type[TableConfig]):
        self.__config = config
        self.__startCursor = self.__config.getStartCursor()
        newTableWorked = self.newTable(site)
        if not newTableWorked:
            raise ValueError("site not valid")

    def newTable(self, site, previouslySelectedButtons = None) -> bool: # Default can't be [] (Would be shared
        setDimensionsWorked = self.__setDimensions(site)                # between calls, Methods are Objects)
        if setDimensionsWorked:
            self.__site = site
            self.cursor = deepcopy(self.__startCursor)
            selectedButtons = [] if previouslySelectedButtons is None else previouslySelectedButtons
            self.selectedButtons = selectedButtons
        return setDimensionsWorked

    def __setDimensions(self, site) -> bool:
        rowsAndColumns = self.__config.getRowsAndColumns(site)
        if rowsAndColumns is not None:
            self.dimensions = {"rows" : rowsAndColumns["rows"], "columns" : rowsAndColumns["columns"]}
            self.__rowContents = rowsAndColumns["rowContents"]
            self.__columnContents = rowsAndColumns["columnContents"]
            return True
        return False

    def getRowContents(self):
        return deepcopy(self.__rowContents)

    def getColumnContents(self):
        return deepcopy(self.__columnContents)

    def getCurrentSite(self):
        return deepcopy(self.__site)

    def getCursorVerbose(self) -> str:
        rowContent = self.__getContent("row", self.cursor)
        columnContent = self.__getContent("column", self.cursor)
        return (columnContent + " " + rowContent)

    def getSelectedButtonsVerbose(self) -> List[Dict[str, str]]:
        selectedButtonsVerbose = []
        for button in self.selectedButtons:
            rowContent = self.__getContent("row", button)
            columnContent = self.__getContent("column", button)
            selectedButtonsVerbose.append(deepcopy({"row" : rowContent, "column" : columnContent}))
        return selectedButtonsVerbose

    def __getContent(self, rowOrColumn, tableCoordinatesDict):
        contents = getattr(self, "_TableModel__" + rowOrColumn + "Contents")
        content = contents[tableCoordinatesDict[rowOrColumn] - 1]
        return content

    def getButtonName(self, buttonCoordinates, site = None) -> str:
        if None == site:
            site = self.__site
        rowsAndColumns = self.__config.getRowsAndColumns(site)
        rows = rowsAndColumns["rowContents"]
        columns = rowsAndColumns["columnContents"]
        rowIndex = buttonCoordinates["row"] - 1
        columnIndex = buttonCoordinates["column"] - 1
        rowName = rows[rowIndex]
        columnName = columns[columnIndex]
        return (columnName + rowName)

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

    async def selectCurrentButton(self):
        self.__deleteSelectedButtonOnSameRowOrColumnAsCursor()
        self.selectedButtons.append(deepcopy(self.cursor))
        getColumn = lambda button : button["column"]
        self.selectedButtons.sort(reverse = False, key = getColumn)

    def __deleteSelectedButtonOnSameRowOrColumnAsCursor(self):
        elementInSameRowOrColumn = lambda element : (element["row"] == self.cursor["row"]) or\
                                                    (element["column"] == self.cursor["column"])
        self.selectedButtons[:] = filterfalse(elementInSameRowOrColumn, self.selectedButtons)
                            #[:] Notation to change elements of list and not
                            # change attribute to filterfalse object reference