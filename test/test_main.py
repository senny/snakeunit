import sys
import StringIO
import snakeunit
import re

class TestResultTestCase(snakeunit.TestCase):

    def testHasAName(self):
        result = snakeunit.TestResult.passed('testMyExample')
        self.assertEqual('testMyExample', result.name)

    def testKnowsTheNameOfItsTestCase(self):
        result = snakeunit.TestResult.passed('testMyExample')
        result.testCase = TestResultTestCase
        self.assertEqual('TestResultTestCase', result.testCaseName())

    def testSuccessfulResult(self):
        result = snakeunit.TestResult.passed('testExample')
        self.assertEqual(True, result.didPass())
        self.assertEqual(False, result.didFail())
        self.assertEqual(False, result.wasSkipped())

    def testFailedResult(self):
        result = snakeunit.TestResult.failed('testExample', AssertionError('did not work'))
        self.assertEqual(True, result.didFail())
        self.assertEqual(False, result.didPass())
        self.assertEqual(False, result.wasSkipped())

    def testSkippedResult(self):
        result = snakeunit.TestResult.skipped('testExample')
        self.assertEqual(False, result.didFail())
        self.assertEqual(False, result.didPass())
        self.assertEqual(True, result.wasSkipped())

class TestSuiteTestCase(snakeunit.TestCase):

    def prepareSuite(self):
        self.suite = snakeunit.TestSuite()
        self.suite.addResult(snakeunit.TestResult.passed('testAny'))
        self.suite.addResult(snakeunit.TestResult.passed('testAny'))
        self.suite.addResult(snakeunit.TestResult.skipped('testAny'))
        self.suite.addResult(snakeunit.TestResult.failed('testFifthRed', AssertionError('some failure')))

    def testCountsTotalResults(self):
        self.prepareSuite()
        self.assertEqual(4, self.suite.totalCount())

    def testCountsPassedResults(self):
        self.prepareSuite()
        self.assertEqual(2, self.suite.passedCount())

    def testCountsFailedResults(self):
        self.prepareSuite()
        self.assertEqual(1, self.suite.failedCount())

    def testCountsSkippedResults(self):
        self.prepareSuite()
        self.assertEqual(1, self.suite.skippedCount())

class ConsoleFormatterTestCase(snakeunit.TestCase):

    def testExecutedPrintsProgress(self):
        output = StringIO.StringIO()
        formatter = snakeunit.ConsoleFormatter(output)
        formatter.testExecuted(snakeunit.TestResult.passed('testFirstGreen'))
        formatter.testExecuted(snakeunit.TestResult.passed('testSecondGreen'))
        formatter.testExecuted(snakeunit.TestResult.skipped('testThirdSkipped'))
        formatter.testExecuted(snakeunit.TestResult.passed('testFourthGreen'))
        formatter.testExecuted(snakeunit.TestResult.failed('testFifthRed', AssertionError('some failure')))

        self.assertEqual("..S.F", output.getvalue())

    def testPrintsSummary(self):
        output = StringIO.StringIO()
        formatter = snakeunit.ConsoleFormatter(output)
        formatter.suiteFinished(snakeunit.TestSuite([snakeunit.TestResult.passed('testFirstGreen'),
                                                     snakeunit.TestResult.skipped('testSecondSkipped'),
                                                     snakeunit.TestResult.failed('testThirdRed', AssertionError('some failure'))]))

        regexp = re.compile(re.escape('3 tests executed (Passed: 1, Skipped: 1, Failed: 1)'))
        self.assertEqual(False, not regexp.search(output.getvalue()), output.getvalue())

    def testPrintsFailedTestsInTheSummary(self):
        output = StringIO.StringIO()
        formatter = snakeunit.ConsoleFormatter(output)
        failedResult = snakeunit.TestResult.failed('testThirdRed', AssertionError('1!=2'))
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
            # terminate somehow
            print "FAILED!"

    class FailingTestCase(snakeunit.TestCase):
        def testFailure(self):
            self.assertEqual(False, True)

        def testAssertKeywordWorks(self):
            assert False

    def testSingleTestCase(self):
        output = StringIO.StringIO()
        runner = snakeunit.Runner(snakeunit.ConsoleFormatter(output))
        runner.register(RunnerTestCase.PassingTestCase)
        runner.register(RunnerTestCase.FailingTestCase)
        runner.run()
        # this test is order dependent...
        progressOutput = output.getvalue().split("\n")[0]
        self.assertEqual("S.FF", progressOutput)

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
            # terminate somehow
            print "FAILED!"
        except AssertionError:
            None

from snakeunit import autorun
