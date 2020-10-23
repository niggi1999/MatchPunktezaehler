#!/usr/bin/env python
from badminton import Badminton
class GameFactory():
    @classmethod
    def create(cls, specificGameName):
        if ("badminton" == specificGameName):
            return Badminton()
        else:
            raise ValueError(specificGameName)