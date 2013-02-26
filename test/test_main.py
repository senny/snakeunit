import sys
import StringIO
import snakeunit

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

class RunnerTestCase(snakeunit.TestCase):

    class ExampleTest(snakeunit.TestCase):
        def testSuccess(self):
            self.assertEqual(True, True)

        def testFailure(self):
            self.assertEqual(False, True)

    def testSingleTestCase(self):
        output = StringIO.StringIO()
        runner = snakeunit.Runner(output)
        runner.register(RunnerTestCase.ExampleTest)
        runner.run()
        self.assertEqual("F.", output.getvalue().split("\n")[0])

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
        except snakeunit.FailedAssertion:
            None


runner = snakeunit.Runner()
runner.register(MainTestCase)
runner.register(TestResultTestCase)
runner.register(AssertionsTestCase)
runner.register(RunnerTestCase)
runner.run()
