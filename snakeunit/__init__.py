"""
Python unit testing framework, written to learn Python.
"""

import re

class TestCase:
    TEST_NAME_REGEXP = re.compile('^test')

    def __init__(self):
        print "created testcase"

    def _tests(self):
        tests = {}
        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method) and TestCase.TEST_NAME_REGEXP.match(method_name):
                tests[method_name] = method

        return tests;

    @classmethod
    def run(klass):
        instance = klass();
        for name, test in instance._tests().items():
            test()
