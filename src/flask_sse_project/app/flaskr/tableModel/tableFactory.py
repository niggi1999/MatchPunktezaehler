from .tableModel import TableModel
from .tableConfig import TableProdConfig

class TableFactory():
    def __init__(self, configClass = TableProdConfig):
        self.configClass = configClass
        self.currentSite = self.configClass.getFirstSite()

    def create(self, configClass = TableProdConfig):
        return TableModel(self.configClass, self.currentSite)
