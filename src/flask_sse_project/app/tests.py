#!/usr/bin/env python
import unittest
from badminton import *

class TestClass(unittest.TestCase):
    def testBadmintonExists(self):
        badminton = Badminton()
        self.assertIsInstance(badminton, Badminton)

    def testCounterStartsAtZero(self):
        badminton = Badminton()
        testCounter = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

    def testCounterUp(self):
        badminton = Badminton()
        badminton.counterUp(1)
        badminton.counterUp(2)

        testCounter = {"Team1" : 1, "Team2" : 1}
        self.assertDictEqual(badminton.counter, testCounter)
        with self.assertRaises(ValueError):
            badminton.counterUp(3)

    def testRoundEndsTeam1(self):
        badminton = Badminton()
        maxPoints = 21
        for i in range(maxPoints):
            badminton.counterUp(1)

        testWonRounds = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

    def testRoundEndsTeam2(self):
        badminton = Badminton()
        maxPoints = 21
        for i in range(maxPoints):
            badminton.counterUp(2)

        testWonRounds = {"Team1" : 0, "Team2" : 1}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

    def testCounterEqualAt20(self):
        badminton = Badminton()
        pointsTillEqual = 20
        for i in range(pointsTillEqual):
            badminton.counterUp(1)
            badminton.counterUp(2)

        pointsToWin = 2
        for i in range(pointsToWin):
            badminton.counterUp(2)

        testWonRounds = {"Team1" : 0, "Team2" : 1}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

    def testEndsWithAbsoluteEnd(self):
        badminton = Badminton()
        pointsTillAbsoluteEnd = 30
        for i in range(pointsTillAbsoluteEnd):
            badminton.counterUp(1)
            badminton.counterUp(2)

        testWonRounds = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 1}
        self.assertDictEqual(badminton.counter, testCounter)

    def testGameEndsAfter2WonRounds(self):
        badminton = Badminton()
        pointsForWonGame = 21 * 2
        for i in range(pointsForWonGame - 1):
            badminton.counterUp(1)

        testWonGames = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.wonGames, testWonGames)
        testWonRounds = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 20, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

        badminton.counterUp(1)

        testWonGames = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.wonGames, testWonGames)
        testWonRounds = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

        #TODO: Aufschlag, Doppel, Seitenwechsel

if __name__ == '__main__':
    unittest.main()