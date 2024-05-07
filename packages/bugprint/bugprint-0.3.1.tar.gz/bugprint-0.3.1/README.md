# Bugprint Package

**Example Usage**

```python
from bugprint import bp

def example_function():
    print("Inside example_function")
    bp()

def another_function():
    print("Inside another_function")
    bp()

# Call bp() at specific lines in your code
bp()  # Example 1
example_function()
bp()  # Example 2
another_function()
bp()  # Example 3
```
