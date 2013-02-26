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
    def run(klass, output):
        instance = klass();
        for name, test in instance._tests().items():
            try:
                test()
                output.write('.')
            except FailedAssertion:
                output.write('F')
                raise

class Runner:
    def __init__(self, output = sys.stdout):
        self.testCases = []
        self.output = output

    def register(self, testCase):
        self.testCases.append(testCase)

    def run(self):
        for testCase in self.testCases:
            testCase.run(self.output)
        self.output.write("\n")
