# Bugprint Package

You may call `bp_setup(verbose=True)` to buffer the printed message with dashes (`-`) to 80 characters.

**Example Usage**

```python
from bugprint import bp

def add(x, y):
    print(f"Adding {x} + {y} = {x + y}")
    bp()

def subtract(x, y):
    print(f"Subtracting {x} - {y} = {x - y}")
    bp()

# Call bp() at specific lines in your code
bp()
add(1, 2)
bp("Addition Complete")
subtract(5, 4)
bp()
```

**Output**

```
DEBUG: tests.py:14
Adding 1 + 2 = 3
DEBUG: tests.py:7
DEBUG: tests.py:16 Addition Complete
Subtracting 5 - 4 = 1
DEBUG: tests.py:11
DEBUG: tests.py:18
```
