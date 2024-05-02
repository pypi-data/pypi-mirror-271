# stylepy

[![PyPI version](https://badge.fury.io/py/stylepy.svg)](https://badge.fury.io/py/stylepy)

`stylepy` is a Python module that provides utilities for formatting text in various styles and complexities.

## Installation

You can install `stylepy` via pip:

```bash
pip install stylepy
```


## Usage Examples for `stylepy` Module

### Headings

```python
from stylepy import h1, h2, h3, h4, h5, h6

h1("Heading 1")
h2("Heading 2")
h3("Heading 3")
h4("Heading 4")
h5("Heading 5")
h6("Heading 6")
```

### Listings

```python
from stylepy import ordered_list, bullet_list

items = ["Item 1", "Item 2", "Item 3"]
ordered_list(items)
bullet_list(items)
```

### Blockquote

```python
from stylepy import blockquote

items = ["Quote 1", "Quote 2", "Quote 3"]
blockquote(items)
```

### Span

```python
from stylepy import span

span("This text is bold")
```

### Pretty JSON
```python
from stylepy import pretty_json

data = {"key": "value"}
pretty_json(data)
```

### Tabular List
```python
from stylepy import tabular_list

data = [
    ("Header 1", "Header 2"),
    ("Value 1", "Value 2"),
    ("Value 3", "Value 4")
]
tabular_list(data)
```

### Time Complexity

```python
from stylepy import timeComplexity

timeComplexity("O(n^2)", "Worst-case time complexity")
```

### Space Complexity

```python
from stylepy import spaceComplexity

spaceComplexity("O(n)", "Space complexity")
```

