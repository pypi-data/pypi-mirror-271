# Bugprint Package

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
bp()
subtract(5, 4)
bp()
```

**Output**

```
BP DEBUG: tests.py, line 12
Adding 1 + 2 = 3
BP DEBUG: tests.py, line 5
BP DEBUG: tests.py, line 14
Subtracting 5 - 4 = 1
BP DEBUG: tests.py, line 9
BP DEBUG: tests.py, line 16
```
