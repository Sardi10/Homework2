# tests/test_calculator.py
import pytest
from calculator.calculator import Calculator
from calculator.calculation import Calculation
from calculator.calculations import Calculations

# Test addition with parameterized data.
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (3.5, 2.5, 6.0),
    (-1, -1, -2),
])
def test_add(a: float, b: float, expected: float) -> None:
    assert Calculator.add(a, b) == expected

# Test subtraction.
@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (2, 5, -3),
    (0, 0, 0),
])
def test_subtract(a: float, b: float, expected: float) -> None:
    assert Calculator.subtract(a, b) == expected

# Test multiplication.
@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (-2, 3, -6),
    (0, 5, 0),
])
def test_multiply(a: float, b: float, expected: float) -> None:
    assert Calculator.multiply(a, b) == expected

# Test division.
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (9, 3, 3),
    (7, 2, 3.5),
])
def test_divide(a: float, b: float, expected: float) -> None:
    assert Calculator.divide(a, b) == expected

# Ensure division by zero raises an exception.
def test_divide_by_zero() -> None:
    with pytest.raises(ZeroDivisionError):
        Calculator.divide(10, 0)

# Test the Calculation class for invalid operator.
def test_invalid_operator() -> None:
    with pytest.raises(ValueError) as exc_info:
        Calculation(1, 2, '^').perform()
    assert "Invalid operator" in str(exc_info.value)

# Test the calculation history functionality.
def test_calculation_history() -> None:
    calc1 = Calculation(1, 2, '+')
    calc1.perform()
    calc2 = Calculation(5, 3, '-')
    calc2.perform()
    history = Calculations()
    history.add_calculation(calc1)
    history.add_calculation(calc2)
    # Verify that the last calculation is correct.
    assert str(history.get_last()) == "5 - 3 = 2"
    history.clear_history()
    with pytest.raises(IndexError):
        history.get_last()

# Test building history from a list of operations using from_operations.
@pytest.mark.parametrize("operations, expected_results", [
    (
        [(1, '+', 2), (5, '-', 3), (3, '*', 4), (10, '/', 2)],
        [3, 2, 12, 5]
    )
])
def test_calculations_from_operations(operations, expected_results) -> None:
    calculations = Calculations.from_operations(operations)
    results = [calc.result for calc in calculations.history]
    assert results == expected_results

def test_show_history(capsys):
    """
    Test that the history shows the correct calculations.
    This test creates several Calculation instances, adds them
    to the history, prints them, and then verifies that the output
    matches the expected strings.
    """
    # Create and perform several calculations.
    calc1 = Calculation(1, 2, '+')
    calc1.perform()  # 1 + 2 = 3
    calc2 = Calculation(5, 3, '-')
    calc2.perform()  # 5 - 3 = 2
    calc3 = Calculation(4, 2, '*')
    calc3.perform()  # 4 * 2 = 8

    # Create a Calculations history and add these calculations.
    history = Calculations()
    history.add_calculation(calc1)
    history.add_calculation(calc2)
    history.add_calculation(calc3)

    # "Show" the history by printing each Calculation.
    for calc in history.history:
        print(calc)

    # Capture the printed output.
    captured_output = capsys.readouterr().out.splitlines()

    # Define the expected output strings.
    expected_output = [
        "1 + 2 = 3",
        "5 - 3 = 2",
        "4 * 2 = 8"
    ]
    
    # Assert that the captured output matches the expected output.
    assert captured_output == expected_output
