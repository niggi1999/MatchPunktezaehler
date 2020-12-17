from .tableFactory import TableFactory
from .abstractModel import AbstractModel

class DialogModel(AbstractModel):
    def __init__(self):
        self.__tableModel = TableFactory.create("newGameDialog")

    def ok(self):
        pass