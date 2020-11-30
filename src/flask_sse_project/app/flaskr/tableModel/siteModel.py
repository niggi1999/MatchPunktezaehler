from .tableFactory import TableFactory
from .tableConfig import TableProdConfig

class SiteModel():
    def __init__(self):
        self.__site = TableProdConfig.getFirstSite()
        self.__tableModel = TableFactory.create(self.__site)