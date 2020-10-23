#!/usr/bin/env python
import unittest
from badminton import *
from gameFactory import *
from model import *

class TestBadminton(unittest.TestCase):
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
        pointsTillOvertime = 20
        for i in range(pointsTillOvertime):
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

    def testUndo(self):
        badminton = Badminton()
        pointsForWonGameAndRound = 21 * 3
        for i in range(pointsForWonGameAndRound):
            badminton.counterUp(1)
        pointsTillOvertime = 20
        for i in range(pointsTillOvertime):
            badminton.counterUp(1)
            badminton.counterUp(2)

        counterUpBy2 = 2
        for i in range(counterUpBy2):
            badminton.counterUp(1)
        counterDownBy2 = 2
        for i in range(counterDownBy2):
            badminton.undo()

        testWonGames = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.wonGames, testWonGames)
        testWonRounds = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 20, "Team2" : 20}
        self.assertDictEqual(badminton.counter, testCounter)
        maxPointsEqualAt20 = 22
        self.assertEqual(badminton.currentMaxPoints, maxPointsEqualAt20)

    def testUndoEmptyStack(self):
        badminton = Badminton()
        with self.assertRaises(ValueError):
            badminton.undo()

    def testRedo(self):
        badminton = Badminton()

        counterUpBy2 = 2
        for i in range(counterUpBy2):
            badminton.counterUp(1)
        undo2 = 2
        for i in range(undo2):
            badminton.undo()
        redo2 = 2
        for i in range(redo2):
            badminton.redo()

        testCounter = {"Team1" : 2, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

    def testRedoEmptyStack(self):
        badminton = Badminton()
        with self.assertRaises(ValueError):
            badminton.redo()

class TestGameFactoy(unittest.TestCase):
    def testGameFactoryWorks(self):
        badminton = GameFactory.create("badminton")
        badminton.counterUp(1)

        testCounter = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

class TestModel(unittest.TestCase):
    def testModelStartWorks(self):
        model = Model()
        model.startGame("badminton")

        self.assertIsInstance(model.game, Badminton)



#TODO: Aufschlag, Doppel, Seitenwechsel

if __name__ == '__main__':
    unittest.main()