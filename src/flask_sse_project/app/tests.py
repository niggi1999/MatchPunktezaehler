#!/usr/bin/env python
import unittest
from flaskr import Badminton, ServePosition, GameFactory, Controller, TableTestConfig, TableModel, TableFactory

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

    def testLastChanged(self):
        badminton = Badminton()

        lastChanged = badminton.gameState()["lastChanged"]
        self.assertEqual(None, lastChanged)

        badminton.counterUp(1)
        lastChanged = badminton.gameState()["lastChanged"]
        self.assertEqual("Team1", lastChanged)

        badminton.counterUp(2)
        lastChanged = badminton.gameState()["lastChanged"]
        self.assertEqual("Team2", lastChanged)

        '''
        badminton.undo()
        lastChanged = badminton.gameState()["counter"]["lastChanged"]
        self.assertEqual("Team2", lastChanged)

        badminton.redo()
        lastChanged = badminton.gameState()["counter"]["lastChanged"]
        self.assertEqual("Team2", lastChanged)
        '''

    def testServePosition(self):
        badminton = Badminton()
        servePositionCorrect = False
        firstServe = badminton.servePosition()
        if(firstServe == ServePosition.TEAM1RIGHT): servePositionCorrect = True
        if(firstServe == ServePosition.TEAM2RIGHT): servePositionCorrect = True
        self.assertEqual(servePositionCorrect, True)
        badminton.counterUp(1)
        servePosition1 = ServePosition.TEAM1LEFT
        self.assertEqual(badminton.servePosition(), servePosition1)
        badminton.counterUp(2)
        servePosition2 = ServePosition.TEAM2LEFT
        self.assertEqual(badminton.servePosition(), servePosition2)
        badminton.counterUp(1)
        servePosition3 = ServePosition.TEAM1RIGHT
        self.assertEqual(badminton.servePosition(), servePosition3)
        badminton.counterUp(2)
        servePosition4 = ServePosition.TEAM2RIGHT
        self.assertEqual(badminton.servePosition(), servePosition4)

    def testSideChange(self):
        badminton = Badminton()
        self.assertEqual(badminton.sidesChanged, False)
        i = 0
        while(i<21):
            badminton.counterUp(1)
            i = i+1
        self.assertEqual(badminton.sidesChanged, True)
        i = 0
        while(i<21):
            badminton.counterUp(2)
            i = i+1
        self.assertEqual(badminton.sidesChanged, False)
        i = 0
        while(i<42):
            badminton.counterUp(1)
            i = i+1
        self.assertEqual(badminton.sidesChanged, False)




class TestGameFactoy(unittest.TestCase):
    def testGameFactoryWorks(self):
        badminton = GameFactory.create("badminton")
        badminton.counterUp(1)

        testCounter = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

class TestController(unittest.TestCase):
    def testControllerStartWorks(self):
        pass

class TestApp(unittest.TestCase):
    def testAppConfig(self):
        pass

class TestTableConfig(unittest.TestCase):
    def testGetNextSite(self):
        self.assertEqual(TableTestConfig.getNextSite("gameMenu"), "game")
        self.assertEqual(TableTestConfig.getNextSite("game"), None)

    def testGetPreviousSite(self):
        self.assertEqual(TableTestConfig.getPreviousSite("playerMenu"), "init")
        self.assertEqual(TableTestConfig.getPreviousSite("init"), None)

    def testRowsAndColumns(self):
        initConfig = TableTestConfig.getRowsAndColumns("init")
        self.assertDictEqual(initConfig, {"rows" : 1, "columns" : 1})

        colorMenuConfig = TableTestConfig.getRowsAndColumns("colorMenu")
        testConfig = {"rows" : 6, "columns" : 2,\
                           "rowContents" : ("Orange", "Red", "Purple", "Blue", "Green", "Black")}
        self.assertDictEqual(colorMenuConfig, testConfig)

    def testGetFirstSite(self):
        firstSite = TableTestConfig.getFirstSite()
        self.assertEqual(firstSite, "init")

    def testGetStartCursor(self):
        startCursor = TableTestConfig.getStartCursor()
        testStartCursor = {"row" : 1, "column" : 1}
        self.assertDictEqual(startCursor, testStartCursor)

class TestTableFactory(unittest.TestCase):
    def testFirstSite(self):
        tableFactory = TableFactory(TableTestConfig)
        self.assertEqual(tableFactory.currentSite, "init")

class TestTableModel(unittest.TestCase):
    def testDimensions(self):
        tableModel = TableModel(TableTestConfig, "colorMenu")
        testConfig = {"rows" : 6, "columns" : 2}
        self.assertDictEqual(testConfig, tableModel.dimensions)

        tableModel._TableModel__newSite("colorMenu", "doubles")
        testConfig = {"rows" : 6, "columns" : 4}
        self.assertDictEqual(testConfig, tableModel.dimensions)


    def testStartCursor(self):
        tableModel = TableModel(TableTestConfig, "colorMenu")
        startCursor = TableTestConfig.getStartCursor()
        self.assertDictEqual(tableModel.cursor, startCursor)

    def testGoDown(self):
        tableModel = TableModel(TableTestConfig, "colorMenu")
        goDownWorked = tableModel.goDown()
        self.assertEqual(goDownWorked, True)
        self.assertEqual(tableModel.cursor["row"], 2)

        for i in range(4):
            tableModel.goDown()
        self.assertEqual(tableModel.cursor["row"], 6)

        goDownWorked = tableModel.goDown()
        self.assertEqual(goDownWorked, False)
        self.assertEqual(tableModel.cursor["row"], 6)

    def testGoUp(self):
        tableModel = TableModel(TableTestConfig, "colorMenu")
        goUpWorked = tableModel.goUp()
        self.assertEqual(goUpWorked, False)
        self.assertEqual(tableModel.cursor["row"], 1)

        tableModel.goDown()
        goUpWorked = tableModel.goUp()
        self.assertEqual(goUpWorked, True)
        self.assertEqual(tableModel.cursor["row"], 1)

    def testGoRight(self):
        tableModel = TableModel(TableTestConfig, "colorMenu")
        goRightWorked = tableModel.goRight()
        self.assertEqual(goRightWorked, True)
        self.assertEqual(tableModel.cursor["column"], 2)

        goRightWorked = tableModel.goRight()
        self.assertEqual(goRightWorked, False)
        self.assertEqual(tableModel.cursor["column"], 2)

    def testGoLeft(self):
        tableModel = TableModel(TableTestConfig, "colorMenu")
        goLeftWorked = tableModel.goLeft()
        self.assertEqual(goLeftWorked, False)
        self.assertEqual(tableModel.cursor["column"], 1)

        tableModel.goRight()
        goLeftWorked = tableModel.goLeft()
        self.assertEqual(goLeftWorked, True)
        self.assertEqual(tableModel.cursor["column"], 1)

    def testSelectButton(self):
        tableModel = TableModel(TableTestConfig, "colorMenu")
        selectWorked = tableModel.selectCurrentButton()
        self.assertEqual(selectWorked, True)
        selectedFields = [{"row" : 1, "column" : 1}]
        self.assertListEqual(tableModel.selectedButtons, selectedFields)

        tableModel.goDown()
        tableModel.selectCurrentButton()
        selectedFields = [{"row" : 2, "column" : 1}]
        self.assertListEqual(tableModel.selectedButtons, selectedFields)

        tableModel.goRight()
        tableModel.selectCurrentButton()
        selectedFields = [{"row" : 2, "column" : 2}]
        self.assertListEqual(tableModel.selectedButtons, selectedFields)

        tableModel.goLeft()
        tableModel.goUp()
        tableModel.selectCurrentButton()
        selectedFields = [{"row" : 2, "column" : 2}, {"row" : 1, "column" : 1}]
        self.assertListEqual(tableModel.selectedButtons, selectedFields)

if __name__ == '__main__':
    unittest.main()