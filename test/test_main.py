import sys
import StringIO
import snakeunit

class MainTestCase(snakeunit.TestCase):

    def testFirst(self):
        None

    def testSecond(self):
        None

class RunnerTestCase(snakeunit.TestCase):

    class ExampleTest(snakeunit.TestCase):
        def testTruth(self):
            self.assertEqual(True, True)

    def testSingleTestCase(self):
        output = StringIO.StringIO()
        runner = snakeunit.Runner(output)
        runner.register(RunnerTestCase.ExampleTest)
        runner.run()
        self.assertEqual(".\n", output.getvalue())

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
runner.register(AssertionsTestCase)
runner.register(RunnerTestCase)
runner.run()
