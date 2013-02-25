import snakeunit

class MainTestCase(snakeunit.TestCase):

    def testFirst(self):
        print "first"

    def testSecond(self):
        print "second"

MainTestCase.run()
