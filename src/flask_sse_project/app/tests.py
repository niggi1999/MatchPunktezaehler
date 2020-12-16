#!/usr/bin/env python
from subprocess import Popen
import unittest
import asyncio
from unittest.mock import patch
from flaskr import Badminton, ServePosition, GameFactory, Controller, TableTestConfig,\
                   TableModel, TableFactory, BluetoothController, create_controller, SiteModel,\
                   SiteTestConfig
from flask_sse import ServerSentEventsBlueprint

from copy import deepcopy

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
        for _ in range(maxPoints):
            badminton.counterUp(1)

        testWonRounds = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

    def testRoundEndsTeam2(self):
        badminton = Badminton()
        maxPoints = 21
        for _ in range(maxPoints):
            badminton.counterUp(2)

        testWonRounds = {"Team1" : 0, "Team2" : 1}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

    def testCounterEqualAt20(self):
        badminton = Badminton()
        pointsTillOvertime = 20
        for _ in range(pointsTillOvertime):
            badminton.counterUp(1)
            badminton.counterUp(2)

        pointsToWin = 2
        for _ in range(pointsToWin):
            badminton.counterUp(2)

        testWonRounds = {"Team1" : 0, "Team2" : 1}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

    def testEndsWithAbsoluteEnd(self):
        badminton = Badminton()
        pointsTillAbsoluteEnd = 30
        for _ in range(pointsTillAbsoluteEnd):
            badminton.counterUp(1)
            badminton.counterUp(2)

        testWonRounds = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.wonRounds, testWonRounds)
        testCounter = {"Team1" : 0, "Team2" : 1}
        self.assertDictEqual(badminton.counter, testCounter)

    def testGameEndsAfter2WonRounds(self):
        badminton = Badminton()
        pointsForWonGame = 21 * 2
        for _ in range(pointsForWonGame - 1):
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
        for _ in range(pointsForWonGameAndRound):
            badminton.counterUp(1)
        pointsTillOvertime = 20
        for _ in range(pointsTillOvertime):
            badminton.counterUp(1)
            badminton.counterUp(2)

        counterUpBy2 = 2
        for _ in range(counterUpBy2):
            badminton.counterUp(1)
        counterDownBy2 = 2
        for _ in range(counterDownBy2):
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
        for _ in range(counterUpBy2):
            badminton.counterUp(1)
        undo2 = 2
        for _ in range(undo2):
            badminton.undo()
        redo2 = 2
        for _ in range(redo2):
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
        firstServe = badminton.updateServePosition()
        if(firstServe == ServePosition.TEAM1RIGHT): servePositionCorrect = True
        if(firstServe == ServePosition.TEAM2RIGHT): servePositionCorrect = True
        self.assertEqual(servePositionCorrect, True)
        badminton.counterUp(1)
        servePosition1 = ServePosition.TEAM1LEFT
        self.assertEqual(badminton.updateServePosition(), servePosition1)
        badminton.counterUp(2)
        servePosition2 = ServePosition.TEAM2LEFT
        self.assertEqual(badminton.updateServePosition(), servePosition2)
        badminton.counterUp(1)
        servePosition3 = ServePosition.TEAM1RIGHT
        self.assertEqual(badminton.updateServePosition(), servePosition3)
        badminton.counterUp(2)
        servePosition4 = ServePosition.TEAM2RIGHT
        self.assertEqual(badminton.updateServePosition(), servePosition4)

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
            i= i+1
        self.assertEqual(badminton.sidesChanged, False)
        i = 0
        while(i<42):
            badminton.counterUp(1)
            i = i+1
        self.assertEqual(badminton.sidesChanged, False)

    def testPlayerPositionWithinTeam(self):
        badminton = Badminton()
        firstPlayerPositions = badminton.playerPositions
        if(ServePosition.TEAM2RIGHT == badminton.servePosition):
            badminton.counterUp(1)
        self.assertEqual(badminton.playerPositions, firstPlayerPositions)
        badminton.counterUp(1)
        currentPositions1 = badminton.playerPositions
        self.assertEqual(currentPositions1["Team1"]["Player1"], firstPlayerPositions["Team1"]["Player2"])
        self.assertEqual(currentPositions1["Team1"]["Player2"], firstPlayerPositions["Team1"]["Player1"])
        badminton.counterUp(2)
        self.assertEqual(badminton.playerPositions, currentPositions1)
        badminton.counterUp(2)
        currentPositions2 = badminton.playerPositions
        self.assertEqual(currentPositions2["Team2"]["Player1"], currentPositions1["Team2"]["Player2"])
        self.assertEqual(currentPositions2["Team2"]["Player2"], currentPositions1["Team2"]["Player1"])

    def testPlayerPositionSideChanged(self):
        badminton = Badminton()
        if(ServePosition.TEAM1RIGHT == badminton.servePosition):
            badminton.counterUp(2)
        pointsToWin = 21
        for _ in range(pointsToWin):
            badminton.counterUp(1)
        currentPositions1 = badminton.playerPositions
        self.assertEqual(currentPositions1["Team1"]["Player1"], 3)
        self.assertEqual(currentPositions1["Team1"]["Player2"], 4)
        self.assertEqual(currentPositions1["Team2"]["Player1"], 1)
        self.assertEqual(currentPositions1["Team2"]["Player2"], 2)
    
    def testGetAbsoluteServePosition(self):
        badminton = Badminton()
        badminton.servePosition = ServePosition.TEAM1LEFT
        self.assertEqual(badminton.getAbsoluteServePosition(), 1)
        badminton.servePosition = ServePosition.TEAM1RIGHT
        self.assertEqual(badminton.getAbsoluteServePosition(), 2)
        badminton.servePosition = ServePosition.TEAM2LEFT
        self.assertEqual(badminton.getAbsoluteServePosition(), 3)
        badminton.servePosition = ServePosition.TEAM2RIGHT
        self.assertEqual(badminton.getAbsoluteServePosition(), 4)
        badminton = Badminton()
        if(ServePosition.TEAM1RIGHT == badminton.servePosition):
            badminton.counterUp(2)
        for _ in range(21):
            badminton.counterUp(1)
        self.assertEqual(badminton.getAbsoluteServePosition(), 4)
        badminton.counterUp(1)
        self.assertEqual(badminton.getAbsoluteServePosition(), 3)




class TestGameFactoy(unittest.TestCase):
    def testGameFactoryWorks(self):
        badminton = GameFactory.create("badminton")
        badminton.counterUp(1)

        testCounter = {"Team1" : 1, "Team2" : 0}
        self.assertDictEqual(badminton.counter, testCounter)

class TestController(unittest.TestCase):
    '''
    @patch("flask_sse.ServerSentEventsBlueprint", autospec = True)
    def testControllerStartWorks(self, mockSse):
        class MockBluetoothController(BluetoothController):
            def __init__(self, testController):
                super().__init__()
                self.testController = testController
                self.counter = 0
            async def readBluetooth(self):
                yield "left" #Call counter
                self.counter += 1
                self.counter += 1
                self.counter += 1
            async def waitForThreadEnd(self):
                while 3 > self.counter:
                    pass

        testBluetoothController = MockBluetoothController(self)
        controller = create_controller(mockSse, testBluetoothController)
        await testBluetoothController.waitForThreadEnd()
        controller.game.get
        controller.assertEqual()
        '''

class TestApp(unittest.TestCase):
    '''
    def testAppConfig(self):
        pass

    @patch.object(BluetoothController, "readBluetooth", autospec = True)
    def testSSEOutput(self, mockReadBluetooth):
        async def sideEffectReadBluetooth(self):
            yield "left"
            self.assertEqual()
            yield "left"
        mockReadBluetooth.side_effect = sideEffectReadBluetooth
        server = Popen(["gunicorn", '"flaskr:create_app()"', "--worker-class" "gevent", "--bind 127.0.0.1:5000"])

        server.kill()
    '''

class TestTableConfig(unittest.TestCase):
    def testGetNextElement(self):
        self.assertEqual(TableTestConfig.getNextElement("gameMenu", "succession"), None)
        self.assertEqual(TableTestConfig.getNextElement("colorMenu", "succession"), "gameMenu")

    def testGetPreviousElement(self):
        self.assertEqual(TableTestConfig.getPreviousElement("playerMenu", "succession"), "init")
        self.assertEqual(TableTestConfig.getPreviousElement("init", "succession"), None)

    def testRowsAndColumns(self):
        initConfig = TableTestConfig.getRowsAndColumns("init")
        self.assertDictEqual(initConfig, {"rows" : 1, "columns" : 1,\
                                          "rowContents" : ("deviceCountTEST",),\
                                          "columnContents" : ("deviceCount",)})

        colorMenuConfig = TableTestConfig.getRowsAndColumns("colorMenuSingles")
        testConfig = {"rows" : 6, "columns" : 2,\
                           "rowContents" : ("orange", "red", "purple", "blue", "green", "black"),
                           "columnContents" : ("team1", "team2")}
        self.assertDictEqual(colorMenuConfig, testConfig)

    def testGetFirstSite(self):
        firstSite = TableTestConfig.getFirstSite()
        self.assertEqual(firstSite, "init")

    def testGetStartCursor(self):
        startCursor = TableTestConfig.getStartCursor()
        testStartCursor = {"row" : 1, "column" : 1}
        self.assertDictEqual(startCursor, testStartCursor)

class TestTableFactory(unittest.TestCase):
    def testCreate(self):
        tableModel = TableFactory.create("init", TableTestConfig)
        self.assertEqual(tableModel.getCurrentSite(), "init")

class TestTableModel(unittest.TestCase):
    def testDimensions(self):
        tableModel = TableFactory.create("colorMenuSingles", TableTestConfig)
        testConfig = {"rows" : 6, "columns" : 2}
        self.assertDictEqual(testConfig, tableModel.dimensions)

        tableModel = TableFactory.create("colorMenuDoubles", TableTestConfig)
        testConfig = {"rows" : 6, "columns" : 4}
        self.assertDictEqual(testConfig, tableModel.dimensions)

    def testStartCursor(self):
        tableModel = TableFactory.create("colorMenuSingles", TableTestConfig)
        startCursor = TableTestConfig.getStartCursor()
        self.assertDictEqual(tableModel.cursor, startCursor)

    def testGoDown(self):
        tableModel = TableFactory.create("colorMenuSingles", TableTestConfig)
        goDownWorked = tableModel.goDown()
        self.assertEqual(goDownWorked, True)
        self.assertEqual(tableModel.cursor["row"], 2)

        for _ in range(4):
            tableModel.goDown()
        self.assertEqual(tableModel.cursor["row"], 6)

        goDownWorked = tableModel.goDown()
        self.assertEqual(goDownWorked, False)
        self.assertEqual(tableModel.cursor["row"], 6)

    def testGoUp(self):
        tableModel = TableFactory.create("colorMenuSingles", TableTestConfig)
        goUpWorked = tableModel.goUp()
        self.assertEqual(goUpWorked, False)
        self.assertEqual(tableModel.cursor["row"], 1)

        tableModel.goDown()
        goUpWorked = tableModel.goUp()
        self.assertEqual(goUpWorked, True)
        self.assertEqual(tableModel.cursor["row"], 1)

    def testGoRight(self):
        tableModel = TableFactory.create("colorMenuSingles", TableTestConfig)
        goRightWorked = tableModel.goRight()
        self.assertEqual(goRightWorked, True)
        self.assertEqual(tableModel.cursor["column"], 2)

        goRightWorked = tableModel.goRight()
        self.assertEqual(goRightWorked, False)
        self.assertEqual(tableModel.cursor["column"], 2)

    def testGoLeft(self):
        tableModel = TableFactory.create("colorMenuSingles", TableTestConfig)
        goLeftWorked = tableModel.goLeft()
        self.assertEqual(goLeftWorked, False)
        self.assertEqual(tableModel.cursor["column"], 1)

        tableModel.goRight()
        goLeftWorked = tableModel.goLeft()
        self.assertEqual(goLeftWorked, True)
        self.assertEqual(tableModel.cursor["column"], 1)

    def testSelectButton(self):
        tableModel = TableFactory.create("colorMenuSingles", TableTestConfig)
        self.assertListEqual(tableModel.selectedButtons, [])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tableModel.selectCurrentButton())
        selectedFields = [{"row" : 1, "column" : 1}]
        self.assertListEqual(tableModel.selectedButtons, selectedFields)

        tableModel.goDown()
        loop.run_until_complete(tableModel.selectCurrentButton())
        selectedFields = [{"row" : 2, "column" : 1}]
        self.assertListEqual(tableModel.selectedButtons, selectedFields)

        tableModel.goRight()
        loop.run_until_complete(tableModel.selectCurrentButton())
        selectedFields = [{"row" : 2, "column" : 2}]
        self.assertListEqual(tableModel.selectedButtons, selectedFields)

        tableModel.goLeft()
        tableModel.goUp()
        loop.run_until_complete(tableModel.selectCurrentButton())
        selectedFields = [{"row" : 1, "column" : 1}, {"row" : 2, "column" : 2}] #Also tests sorting
        self.assertListEqual(tableModel.selectedButtons, selectedFields)

    def testCurrentSite(self):
        tableModel = TableFactory.create("gameMenu", TableTestConfig)
        currentSite = tableModel.getCurrentSite()
        self.assertEqual(currentSite, "gameMenu")

    def testNewTable(self):
        tableModel = TableFactory.create("gameMenu", TableTestConfig)
        newTableWorked = tableModel.newTable("init")
        self.assertEqual(newTableWorked, True)
        self.assertEqual(tableModel.getCurrentSite(), "init")

        newTableWorked = tableModel.newTable("nothing")
        self.assertEqual(newTableWorked, False)
        self.assertEqual(tableModel.getCurrentSite(), "init")

    def testGetCursorVerbose(self):
        tableModel = TableFactory.create("init", TableTestConfig)
        cursor = tableModel.getCursorVerbose()
        self.assertEqual(cursor, "deviceCount deviceCountTEST")

    def testGetSelectedButtonsVerbose(self):
        tableModel = TableFactory.create("colorMenuSingles", TableTestConfig)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tableModel.selectCurrentButton())
        selectedButtons = tableModel.getSelectedButtonsVerbose()
        listForComparison = [{"row" : "orange", "column" : "team1"}]
        self.assertListEqual(selectedButtons, listForComparison)

class TestSiteModel(unittest.TestCase):
    def testSiteForward(self):
        siteModel = SiteModel(SiteTestConfig, "colorMenuSingles")
        loop = asyncio.get_event_loop()
        with self.assertRaises(ValueError):
            loop.run_until_complete(siteModel._SiteModel__siteForward())
        self.assertEqual(siteModel._SiteModel__tableModel.getCurrentSite(), "colorMenuSingles")

        siteModel = SiteModel(SiteTestConfig, "colorMenuSingles")
        jumpsToNextButton = 2
        for _ in range(jumpsToNextButton):
            loop.run_until_complete(siteModel.ok())
            siteModel.right()
            siteModel.down()
        loop.run_until_complete(siteModel.ok())
        self.assertEqual(siteModel._SiteModel__tableModel.getCurrentSite(), "gameMenu")
        loop.run_until_complete(siteModel.ok())
        siteModel.right()
        self.assertEqual(siteModel._SiteModel__tableModel.getCurrentSite(), "gameMenu")

    def testSiteBackward(self):
        siteModel = SiteModel(SiteTestConfig)
        loop = asyncio.get_event_loop()
        with self.assertRaises(TypeError):
            loop.run_until_complete(siteModel._SiteModel__siteBackward())
        self.assertEqual(siteModel._SiteModel__tableModel.getCurrentSite(), "init")

        loop.run_until_complete(siteModel._SiteModel__siteForward())
        loop.run_until_complete(siteModel._SiteModel__siteBackward())
        self.assertEqual(siteModel._SiteModel__tableModel.getCurrentSite(), "init")

    def testGetActiveElement(self):
        siteModel = SiteModel(SiteTestConfig)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "nextButton")

        firstSiteStartElementBeforeChange = SiteTestConfig.getAttribute("_firstSiteStartElement")
        SiteTestConfig.setAttribute("_firstSiteStartElement", "table")
        siteModel = SiteModel(SiteTestConfig)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "deviceCount deviceCountTEST")
        SiteTestConfig.setAttribute("_firstSiteStartElement", firstSiteStartElementBeforeChange)

    def testRight(self):
        startElementNewSiteBeforeChange = SiteTestConfig.getAttribute("_startElementNewSite")
        SiteTestConfig.setAttribute("_startElementNewSite", "previousButton")

        siteModel = SiteModel(SiteTestConfig, "playerMenu")
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "previousButton")

        rightWorked = siteModel.right()
        self.assertEqual(rightWorked, True)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "singles mode")

        rightWorked = siteModel.right()
        self.assertEqual(rightWorked, True)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "doubles mode")

        rightWorked = siteModel.right()
        self.assertEqual(rightWorked, True)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "nextButton")

        rightWorked = siteModel.right()
        self.assertEqual(rightWorked, False)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "nextButton")

        SiteTestConfig.setAttribute("_startElementNewSite", startElementNewSiteBeforeChange)

    def testLeft(self):
        siteModel = SiteModel(SiteTestConfig, "playerMenu")
        jumpsToNextButton = 4
        for _ in range(jumpsToNextButton):
            siteModel.right()

        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "nextButton")

        rightWorked = siteModel.left()
        self.assertEqual(rightWorked, True)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "doubles mode")

        rightWorked = siteModel.left()
        self.assertEqual(rightWorked, True)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "singles mode")

        rightWorked = siteModel.left()
        self.assertEqual(rightWorked, True)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "previousButton")

        rightWorked = siteModel.left()
        self.assertEqual(rightWorked, False)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "previousButton")

    def testLeftOnFirstSite(self):
        siteModel = SiteModel(SiteTestConfig)
        moveWorked = siteModel.left()
        self.assertEqual(moveWorked, False)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "nextButton")

    def testDown(self):
        siteModel = SiteModel(SiteTestConfig, "colorMenuSingles")
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "team1 orange")

        moveWorked = siteModel.down()
        self.assertEqual(moveWorked, True)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "team1 red")

        jumpsToEnd = 4
        for _ in range(jumpsToEnd):
            moveWorked = siteModel.down()
            self.assertEqual(moveWorked, True)

        moveWorked = siteModel.down()
        self.assertEqual(moveWorked, False)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "team1 black")

    def testUp(self):
        siteModel = SiteModel(SiteTestConfig, "colorMenuSingles")
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "team1 orange")

        moveWorked = siteModel.up()
        self.assertEqual(moveWorked, False)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "team1 orange")

        jumpsToEnd = 6
        for _ in range(jumpsToEnd):
            siteModel.down()
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "team1 black")

        moveWorked = siteModel.up()
        self.assertEqual(moveWorked, True)
        activeElement = siteModel.getActiveElement()
        self.assertEqual(activeElement, "team1 green")

    def testGoToSameSiteTwice(self):
        siteModel = SiteModel(SiteTestConfig, "playerMenu")
        self.assertEqual(siteModel._SiteModel__tableModel.getCurrentSite(), "playerMenu")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(siteModel._SiteModel__tableModel.selectCurrentButton())
        selectedButtonsBeforeSwitch = siteModel.getSelectedButtonsCurrentSiteVerbose()

        loop.run_until_complete(siteModel._SiteModel__siteForward())
        self.assertEqual(siteModel._SiteModel__tableModel.getCurrentSite(), "colorMenuSingles")
        loop.run_until_complete(siteModel._SiteModel__siteBackward())
        self.assertEqual(siteModel._SiteModel__tableModel.getCurrentSite(), "playerMenu")
        selectedButtonsAfterSwitch = siteModel.getSelectedButtonsCurrentSiteVerbose()

        self.assertListEqual(selectedButtonsBeforeSwitch, selectedButtonsAfterSwitch)

    def testOk(self):
        siteModel = SiteModel(SiteTestConfig, "colorMenuSingles")
        siteModel.left()
        self.assertEqual(siteModel.getActiveElement(), "previousButton")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(siteModel.ok())
        self.assertEqual(siteModel._SiteModel__site, "playerMenu")

        siteModel = SiteModel(SiteTestConfig, "colorMenuSingles")
        jumpsTillNextButton = 2
        for _ in range(jumpsTillNextButton):
            loop.run_until_complete(siteModel.ok())
            siteModel.right()
            siteModel.down()
        self.assertEqual(siteModel.getActiveElement(), "nextButton")
        loop.run_until_complete(siteModel.ok())
        self.assertEqual(siteModel._SiteModel__site, "gameMenu")

        siteModel = SiteModel(SiteTestConfig, "colorMenuSingles")
        loop.run_until_complete(siteModel.ok())
        listForComparison = [{"row" : "orange", "column" : "team1"}]
        self.assertListEqual(siteModel.getSelectedButtonsCurrentSiteVerbose(), listForComparison)

    @patch.object(SiteModel, "_SiteModel__notifyStartGame")
    def testNotify(self, mockNotify):
        siteModel = SiteModel(SiteTestConfig, "gameMenu")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(siteModel.ok())
        siteModel.right()
        loop.run_until_complete(siteModel.ok())
        mockNotify.assert_called_once()

    def testColorMenuDoublesWasSelected(self):
        siteModel = SiteModel(SiteTestConfig, "playerMenu")
        siteModel._SiteModel__tableModel.selectedButtons = [{"row" : 1, "column" : 2},]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(siteModel._SiteModel__siteForward())
        self.assertEqual(siteModel._SiteModel__site, "colorMenuDoubles")

if __name__ == '__main__':
    unittest.main()