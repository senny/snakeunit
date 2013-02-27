# SnakeUnit

This code was written to learn Python, don't expect something useful.

## Usage

```python
import snakeunit

class CalculatorTestCase(snakeunit.TestCase):

    def setup(self):
        self.calculator = Calculator()

    def testAdd(self):
        self.assertEqual(3, self.calculator.add(1, 2), "1 + 2 should = 3")

    def testDivision(self):
        self.skip();
        self.assertEqual(2, self.calculator.divide(4, 2), "4 / 2 should = 2")
```

to run your test cases you can either register them with a runner
instance:

```python
runner = snakeunit.Runner()
self.runner.register(CalculatorTestCase)
self.runner.run()
```

If you don't want to register every test case manually you can tell
the `Runner` to run all test cases. Snakeunit will then find and run
all loaded test cases:

```python
# this will run all your test cases
from snakeunit import autorun
```

The output of a test run is as follows:

```
...................

snakeunit finished in 0.102198 seconds
19 tests executed (Passed: 19, Skipped: 0, Failed: 0, Exception: 0)
```
