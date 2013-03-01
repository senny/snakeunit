import StringIO
import snakeunit
import re
from time import sleep

class TestResultTestCase(snakeunit.TestCase):

    def testHasAName(self):
        result = snakeunit.TestResult('testMyExample', 'passed')
        self.assertEqual('testMyExample', result.name)

    def testKnowsTheNameOfItsTestCase(self):
        result = snakeunit.TestResult('testMyExample', 'passed')
        result.testCase = TestResultTestCase
        self.assertEqual('TestResultTestCase', result.testCaseName())

    def testSuccessfulResult(self):
        result = snakeunit.TestResult('testExample', 'passed')
        self.assertEqual(True, result.didPass())

    def testFailedResult(self):
        result = snakeunit.TestResult('testExample', 'failed', AssertionError('did not work'))
        self.assertEqual(False, result.didPass())

    def testSkippedResult(self):
        result = snakeunit.TestResult('testExample', 'skipped')
        self.assertEqual(False, result.didPass())

    def testExceptionResult(self):
        result = snakeunit.TestResult('testExample', 'exception')
        self.assertEqual(False, result.didPass())


class TestSuiteTestCase(snakeunit.TestCase):

    def setup(self):
        self.suite = snakeunit.TestSuite()
        self.suite.addResult(snakeunit.TestResult('testAny', 'passed'))
        self.suite.addResult(snakeunit.TestResult('testAny', 'passed'))
        self.suite.addResult(snakeunit.TestResult('testAny', 'skipped'))
        self.suite.addResult(snakeunit.TestResult('testFifthRed', 'failed', AssertionError('some failure')))

    def testCountsTotalResults(self):
        self.assertEqual(4, self.suite.totalCount())

    def testCountsResultsByState(self):
        self.assertEqual(2, self.suite.count('passed'))
        self.assertEqual(1, self.suite.count('failed'))
        self.assertEqual(1, self.suite.count('skipped'))

    def testExecutionTimeStartsAtZero(self):
        self.assertEqual(0, self.suite.totalTime())

    def testMeasuersExecutionTime(self):
        sleepTime = 0.1
        self.suite.start()
        sleep(sleepTime)
        self.suite.finish()
        self.assertEqual(True, self.suite.totalTime() > sleepTime,
                         "total time %s should be bigger than sleep time of %s" % (self.suite.totalTime(), sleepTime))

class ConsoleFormatterTestCase(snakeunit.TestCase):

    def testExecutedPrintsProgress(self):
        output = StringIO.StringIO()
        formatter = snakeunit.ConsoleFormatter(output)
        formatter.testExecuted(snakeunit.TestResult('testFirstGreen', 'passed'))
        formatter.testExecuted(snakeunit.TestResult('testSecondGreen', 'passed'))
        formatter.testExecuted(snakeunit.TestResult('testThirdSkipped', 'skipped'))
        formatter.testExecuted(snakeunit.TestResult('testFourthGreen', 'passed'))
        formatter.testExecuted(snakeunit.TestResult('testFifthRed', 'failed', AssertionError('some failure')))

        self.assertEqual("..S.F", output.getvalue())

    def testPrintsSummary(self):
        output = StringIO.StringIO()
        formatter = snakeunit.ConsoleFormatter(output)
        formatter.suiteFinished(snakeunit.TestSuite([snakeunit.TestResult('testFirstGreen', 'passed'),
                                                     snakeunit.TestResult('testSecondSkipped', 'skipped'),
                                                     snakeunit.TestResult('testThirdRed', 'failed', AssertionError('some failure'))]))

        regexp = re.compile(re.escape('3 tests executed (Passed: 1, Skipped: 1, Failed: 1, Exception: 0)'))
        self.assertEqual(False, not regexp.search(output.getvalue()), output.getvalue())

    def testPrintsFailedTestsInTheSummary(self):
        output = StringIO.StringIO()
        formatter = snakeunit.ConsoleFormatter(output)
        failedResult = snakeunit.TestResult('testThirdRed', 'failed', AssertionError('1!=2'))
        failedResult.testCase = ConsoleFormatterTestCase
        formatter.suiteFinished(snakeunit.TestSuite([failedResult]))

        regexp = re.compile(re.escape("1) Failure:\ntestThirdRed(ConsoleFormatterTestCase)\n1!=2"))
        self.assertEqual(False, not regexp.search(output.getvalue()), output.getvalue())

class RunnerTestCase(snakeunit.TestCase):

    class PassingTestCase(snakeunit.TestCase):
        def testSuccess(self):
            self.assertEqual(True, True)

        def testSkipped(self):
            self.skip()
            raise AssertionError('Test should be skipped but was not.')

    class FailingTestCase(snakeunit.TestCase):
        def testFailure(self):
            self.assertEqual(False, True)

        def testException(self):
            raise NameError('HiThere')

        def testAssertKeywordWorks(self):
            assert False

    def setup(self):
        self.output = StringIO.StringIO()
        self.runner = snakeunit.Runner(snakeunit.ConsoleFormatter(self.output))

    def testSingleTestCase(self):
        self.runner.register(RunnerTestCase.PassingTestCase)
        self.runner.register(RunnerTestCase.FailingTestCase)
        self.runner.run()
        # this test is order dependent...
        progressOutput = self.output.getvalue().split("\n")[0]
        self.assertEqual("S.FEF", progressOutput)

    class SetupAndTeardownTestCase(snakeunit.TestCase):
        # HACK: catch the output of the tests somehow...
        buffer = ''

        def setup(self):
            RunnerTestCase.SetupAndTeardownTestCase.buffer += ";SETUP;"

        def teardown(self):
            RunnerTestCase.SetupAndTeardownTestCase.buffer += ";TEARDOWN;"

        def test1(self):
            RunnerTestCase.SetupAndTeardownTestCase.buffer += ";TEST;"

        def test2(self):
            RunnerTestCase.SetupAndTeardownTestCase.buffer += ";TEST;"

    def testSetupAndTeardown(self):
        self.runner.register(RunnerTestCase.SetupAndTeardownTestCase)
        self.runner.run()
        self.assertEqual(";SETUP;;TEST;;TEARDOWN;;SETUP;;TEST;;TEARDOWN;",
                         RunnerTestCase.SetupAndTeardownTestCase.buffer)

class AssertionsTestCase(snakeunit.TestCase):

    def testAssertEqualsWhenEqualInteger(self):
        self.assertEqual(1, 1)

    def testAssertEqualsWhenEqualStrings(self):
        self.assertEqual('hello', 'hello')

    def testAssertEqualsWhenEqualBooleans(self):
        self.assertEqual(True, True)
        self.assertEqual(False, False)

    def testAssertEqualsNotEqual(self):
        try:
            self.assertEqual(1, 2)
        except AssertionError:
            pass
        else:
            raise AssertionError('assertEquals should raise AssertionError but did not.')


from snakeunit import autorun
