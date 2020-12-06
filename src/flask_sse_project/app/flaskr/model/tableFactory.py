from .tableModel import TableModel
from .config import TableProdConfig

class TableFactory():
    @staticmethod
    def create(site, config = TableProdConfig):
        return TableModel(site, config)
