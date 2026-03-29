import pytest

def describe_foo():
    def it_bar():
        # A test that always passes
        assert True
        
    def it_also_passes():
        # Another example to show the nesting
        expected = 10
        actual = 5 + 5
        assert actual == expected