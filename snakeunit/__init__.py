"""
Python unit testing framework, written to learn Python.
"""

import re
import sys

class FailedAssertion(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class TestResult:

    def __init__(self, name, state, exception = None):
        self.name = name
        self.state = state
        self.exception = exception

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

class TestCase:
    TEST_NAME_REGEXP = re.compile('^test')

    def _tests(self):
        tests = {}
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and TestCase.TEST_NAME_REGEXP.match(method_name):
                tests[method_name] = method

        return tests;

    # ASSERTIONS
    def assertEqual(self, expected, actual, message = None):
        if expected != actual:
            message = "expected %s to equal %s but it was not." % (actual, expected) if not message else message
            raise FailedAssertion(message)

    @classmethod
    def run(klass):
        testResults = []
        instance = klass();
        for name, test in instance._tests().items():
            result = None
            try:
                test()
                testResults.append(TestResult.passed(name))
            except FailedAssertion, e:
                testResults.append(TestResult.failed(name, e))

        return testResults

class Runner:
    def __init__(self, output = sys.stdout):
        self.testCases = []
        self.output = output

    def register(self, testCase):
        self.testCases.append(testCase)

    def run(self):
        suiteResults = []
        for testCase in self.testCases:
            results = testCase.run()
            for result in results:
                if result.didPass():
                    self.output.write('.')
                elif result.didFail():
                    self.output.write('F')

            suiteResults.extend(results)

        self.output.write("\n")
        for result in suiteResults:
            if result.didFail():
                self.output.write(result.name + "\n")
                self.output.write(str(result.exception) + "\n")
                self.output.write("\n")
        self.output.write("\n")
