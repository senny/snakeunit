"""
Python unit testing framework, written to learn Python.
"""

import re
import sys
import inspect

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

class TestCase(object):
    TEST_NAME_REGEXP = re.compile('^test')

    def _tests(self):
        tests = {}
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and TestCase.TEST_NAME_REGEXP.match(method_name):
                tests[method_name] = method

        return tests;

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

    def testExecuted(self, result):
        if result.didPass():
            self.output.write('.')
        elif result.didFail():
            self.output.write('F')
        elif result.wasSkipped():
            self.output.write('S')

    def suiteFinished(self, suiteResults):
        self.output.write("\n")
        failedCounter = 0
        indent = ' ' * 2
        self.output.write("\n")
        for result in suiteResults:
            if result.didFail():
                failedCounter += 1
                self.output.write("%s%d) Failure:\n" % (indent, failedCounter))
                self.output.write("%s(%s)\n" % (result.name, result.testCaseName()))
                self.output.write("%s\n" % (str(result.exception)))
                self.output.write("\n")
        total = len(suiteResults)
        passed = sum(1 for res in suiteResults if res.didPass())
        skipped = sum(1 for res in suiteResults if res.wasSkipped())
        failed = sum(1 for res in suiteResults if res.didFail())
        self.output.write("%s tests executed (Passed: %s, Skipped: %s, Failed: %s)\n" % (total, passed, skipped, failed))


class Runner(object):
    def __init__(self, formatter):
        self.testCases = []
        self.output = sys.stdout
        self.formatter = formatter

    def register(self, testCase):
        self.testCases.append(testCase)

    def run(self):
        suiteResults = []
        for testCase in self.testCases:
            testCaseResults = self.runTestCase(testCase)
            suiteResults.extend(testCaseResults)
        self.formatter.suiteFinished(suiteResults)

    def runTestCase(self, testCase):
        results = []
        instance = testCase();
        for name, test in instance._tests().items():
            result = None
            try:
                test()
                result = TestResult.passed(name)
            except AssertionError, e:
                result = TestResult.failed(name, e)
            except TestSkipped:
                result = TestResult.skipped(name)
            result.testCase = testCase
            self.formatter.testExecuted(result)
            results.append(result)

        return results

    @classmethod
    def runAll(klass, formatter = ConsoleFormatter()):
        runner = klass(formatter)
        for testCase in TestCase.__subclasses__():
            # HACK: only run top level classes
            m = inspect.getmodule(testCase)
            if getattr(m, testCase.__name__, []) is testCase:
                runner.register(testCase)
        runner.run()
