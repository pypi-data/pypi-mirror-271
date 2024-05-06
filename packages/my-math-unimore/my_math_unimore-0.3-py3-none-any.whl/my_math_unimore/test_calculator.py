import pytest
from my_math_unimore import MathOperations

@pytest.fixture
def calculator():
    return MathOperations(10, 5)

def test_add(calculator):
    assert calculator.add() == 15

def test_subtract(calculator):
    assert calculator.subtract() == 5

def test_multiply(calculator):
    assert calculator.multiply() == 50

def test_divide(calculator):
    assert calculator.divide() == 2.0

def test_divide_by_zero():
    calculator = MathOperations(10, 0)
    assert calculator.divide() == "Cannot divide by zero"