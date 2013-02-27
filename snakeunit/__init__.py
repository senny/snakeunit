"""
Python unit testing framework, written to learn Python.
"""

import re
import sys
import inspect
from time import time

class TestSkipped(Exception):
    None

class TestResult(object):

    def __init__(self, name, state, exception = None):
        self.name = name
        self.state = state
        self.exception = exception
        self.testCase = None

    def testCaseName(self):
        return self.testCase.__name__ if self.testCase else ''

    def didPass(self):
        return self.state == 'passed'

    def wasSkipped(self):
        return self.state == 'skipped'

    def didFail(self):
        return self.state == 'failed'

    @classmethod
    def skipped(klass, name):
        return klass(name, 'skipped')

    @classmethod
    def passed(klass, name):
        return klass(name, 'passed')

    @classmethod
    def failed(klass, name, exception):
        return klass(name, 'failed', exception)

class TestSuite:
    def __init__(self, results = None):
        self.results = results or []
        self.startedAt = None
        self.finishedAt = None

    def start(self):
        self.startedAt = time()

    def finish(self):
        self.finishedAt = time()

    def totalTime(self):
        if self.finishedAt and self.startedAt:
            return self.finishedAt - self.startedAt
        else:
            return 0

    def addResult(self, result):
        self.results.append(result)

    def totalCount(self):
        return len(self.results)

    def passedCount(self):
        return sum(1 for res in self.results if res.didPass())

    def skippedCount(self):
        return sum(1 for res in self.results if res.wasSkipped())

    def failedCount(self):
        return sum(1 for res in self.results if res.didFail())

class TestCase(object):
    TEST_NAME_REGEXP = re.compile('^test')

    def _tests(self):
        tests = {}
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and TestCase.TEST_NAME_REGEXP.match(method_name):
                tests[method_name] = method

        return tests;

    def setup(self):
        None

    def teardown(self):
        None

    def skip(self):
        raise TestSkipped()

    # ASSERTIONS
    def assertEqual(self, expected, actual, message = None):
        if expected != actual:
            message = "expected %s to equal %s but it was not." % (actual, expected) if not message else message
            raise AssertionError(message)

class ConsoleFormatter(object):

    def __init__(self, output = sys.stdout):
        self.output = output
        self.indent = ' ' * 2

    def writeLn(self, text = ""):
        self.output.write("%s\n" % text)

    def testExecuted(self, result):
        if result.didPass():
            self.output.write('.')
        elif result.didFail():
            self.output.write('F')
        elif result.wasSkipped():
            self.output.write('S')

    def suiteFinished(self, suite):
        self.writeLn()
        self.writeLn()
        failedCounter = 0
        for result in suite.results:
            if result.didFail():
                failedCounter += 1
                self.writeLn("%s%d) Failure:" % (self.indent, failedCounter))
                self.writeLn("%s(%s)" % (result.name, result.testCaseName()))
                self.writeLn("%s\n" % (str(result.exception)))
                self.writeLn()
        self.writeLn("snakeunit finished in %f seconds" % suite.totalTime())
        self.writeLn("%s tests executed (Passed: %s, Skipped: %s, Failed: %s)" % (suite.totalCount(),
                                                                                  suite.passedCount(),
                                                                                  suite.skippedCount(),
                                                                                  suite.failedCount()))
class Runner(object):
    def __init__(self, formatter):
        self.testCases = []
        self.output = sys.stdout
        self.formatter = formatter
        self.testSuite = None

    def register(self, testCase):
        self.testCases.append(testCase)

    def run(self):
        self.testSuite = TestSuite()
        self.testSuite.start()
        for testCase in self.testCases:
            self.runTestCase(testCase)
        self.testSuite.finish()

        self.formatter.suiteFinished(self.testSuite)

    def runTest(self, testCase, test, name):
        testCase.setup()
        try:
            test()
            return TestResult.passed(name)
        except AssertionError, e:
            return TestResult.failed(name, e)
        except TestSkipped:
            return TestResult.skipped(name)
        finally:
            testCase.teardown()

    def runTestCase(self, testCase):
        instance = testCase();
        for name, test in instance._tests().items():
            result = self.runTest(instance, test, name)
            result.testCase = testCase
            self.formatter.testExecuted(result)
            self.testSuite.addResult(result)

    @classmethod
    def runAll(klass, formatter = ConsoleFormatter()):
        runner = klass(formatter)
        for testCase in TestCase.__subclasses__():
            # HACK: only run top level classes
            module = inspect.getmodule(testCase)
            if getattr(module, testCase.__name__, []) is testCase:
                runner.register(testCase)
        runner.run()
