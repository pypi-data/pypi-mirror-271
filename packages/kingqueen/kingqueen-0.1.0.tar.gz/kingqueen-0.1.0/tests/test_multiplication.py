
# tests/test_multiplication.py
from multiplication.multiplication import multiply_two_variables, multiply_three_variables

def test_multiply_two_variables():
    assert multiply_two_variables(2, 3) == 6
    assert multiply_two_variables(5, -4) == -20
    assert multiply_two_variables(0, 10) == 0

def test_multiply_three_variables():
    assert multiply_three_variables(2, 3, 4) == 24
    assert multiply_three_variables(5, -4, 2) == -40
    assert multiply_three_variables(0, 10, 5) == 0

