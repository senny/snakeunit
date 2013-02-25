import snakeunit

class MainTestCase(snakeunit.TestCase):

    def testFirst(self):
        None

    def testSecond(self):
        None

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

MainTestCase.run()
AssertionsTestCase.run()
