#!/usr/bin/env python
import unittest
from badminton import *

class TestClass(unittest.TestCase):
    def testBadmintonExists(self):
        badminton = Badminton()
        self.assertIsInstance(badminton, Badminton)

    def testCounterStartsAtZero(self):
        badminton = Badminton()
        self.assertEqual(badminton.counterTeam1, 0)
        self.assertEqual(badminton.counterTeam2, 0)

    def testCounterUp(self):
        badminton = Badminton()
        badminton.counterUp(1)
        badminton.counterUp(2)
        self.assertEqual(badminton.counterTeam1, 1)
        self.assertEqual(badminton.counterTeam2, 1)
        with self.assertRaises(ValueError):
            badminton.counterUp(3)

    def testRoundEndsTeam1(self):
        badminton = Badminton()
        maxPoints = 21
        for i in range(maxPoints):
            badminton.counterUp(1)
        self.assertEqual(badminton.wonRoundsTeam1, 1)
        self.assertEqual(badminton.wonRoundsTeam2, 0)
        self.assertEqual(badminton.counterTeam1, 0)
        self.assertEqual(badminton.counterTeam2, 0)

    def testRoundEndsTeam2(self):
        badminton = Badminton()
        maxPoints = 21
        for i in range(maxPoints):
            badminton.counterUp(2)
        self.assertEqual(badminton.wonRoundsTeam2, 1)
        self.assertEqual(badminton.wonRoundsTeam1, 0)
        self.assertEqual(badminton.counterTeam1, 0)
        self.assertEqual(badminton.counterTeam2, 0)

    def testCounterEqualAt20(self):
        badminton = Badminton()
        pointsTillEqual = 20
        for i in range(pointsTillEqual):
            badminton.counterUp(1)
            badminton.counterUp(2)

        pointsToWin = 2
        for i in range(pointsToWin):
            badminton.counterUp(2)

        self.assertEqual(badminton.wonRoundsTeam2, 1)
        self.assertEqual(badminton.wonRoundsTeam1, 0)
        self.assertEqual(badminton.counterTeam1, 0)
        self.assertEqual(badminton.counterTeam2, 0)




if __name__ == '__main__':
    unittest.main()