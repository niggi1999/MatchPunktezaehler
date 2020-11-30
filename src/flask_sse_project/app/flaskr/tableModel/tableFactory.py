from .tableModel import TableModel
from .tableConfig import TableProdConfig

class TableFactory():
    @staticmethod
    def create(site, configClass = TableProdConfig):
        return TableModel(site, configClass)
