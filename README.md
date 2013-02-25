# SnakeUnit

## Usage

```python
import snakeunit

class ExampleTestCase(snakeunit.TestCase):

    def setup:
        self.calculator = Calculator()

    def testAdd:
        self.assertEqual(3, self.calculator.add(1, 2), "1 + 2 should = 3")
```
