# Description: Sample pytest file to show how parameterize decorator works
import pytest

# sample test function
def add(a,b):
    return a+b


# test parameter decorator
@pytest.mark.parametrize("a,b,expected", [(1,2,3),(4,5,9),(11,20,30)])
def test_add(a,b,expected):
    assert add(a,b) == expected