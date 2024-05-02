import pytest

from stylepy import h1, h2, h3, h4, h5, h6

def test_h1():
    assert h1("Hello") == "<h1>Hello</h1>", "h1 should wrap text in <h1> tags"

def test_h2():
    assert h2("World") == "<h2>World</h2>", "h2 should wrap text in <h2> tags"

# Add more tests for h3, h4, h5, h6
