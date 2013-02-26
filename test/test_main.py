import sys
import StringIO
import snakeunit
import re

class MainTestCase(snakeunit.TestCase):

    def testFirst(self):
        None

    def testSecond(self):
        None

class TestResultTestCase(snakeunit.TestCase):

    def testHasAName(self):
        result = snakeunit.TestResult.passed('testMyExample')
        self.assertEqual('testMyExample', result.name)

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
        formatter.suiteFinished([snakeunit.TestResult.passed('testFirstGreen'),
                                 snakeunit.TestResult.skipped('testSecondSkipped'),
                                 snakeunit.TestResult.failed('testThirdRed', AssertionError('some failure'))])

        regexp = re.compile('3 tests executed \(Passed: 1, Skipped: 1, Failed: 1\)')
        self.assertEqual(False, not regexp.search(output.getvalue()), output.getvalue())

    def testPrintsFailedTestsInTheSummary(self):
        output = StringIO.StringIO()
        formatter = snakeunit.ConsoleFormatter(output)
        formatter.suiteFinished([snakeunit.TestResult.passed('testFirstGreen'),
                                 snakeunit.TestResult.failed('testThirdRed', AssertionError('1!=2'))])

        regexp = re.compile("1\) Failure:\ntestThirdRed\n1!=2")
        self.assertEqual(False, not regexp.search(output.getvalue()), output.getvalue())


class RunnerTestCase(snakeunit.TestCase):

    class ExampleTest(snakeunit.TestCase):
        def testSuccess(self):
            self.assertEqual(True, True)

        def testFailure(self):
            self.assertEqual(False, True)

        def testSkipped(self):
            self.skip()
            # terminate somehow
            print "FAILED!"

    def testSingleTestCase(self):
        output = StringIO.StringIO()
        runner = snakeunit.Runner(snakeunit.ConsoleFormatter(output))
        runner.register(RunnerTestCase.ExampleTest)
        runner.run()
        # this test is order dependent...
        self.assertEqual("FS.", output.getvalue().split("\n")[0])

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


runner = snakeunit.Runner()
runner.register(MainTestCase)
runner.register(TestResultTestCase)
runner.register(AssertionsTestCase)
runner.register(RunnerTestCase)
runner.register(ConsoleFormatterTestCase)
runner.run()
