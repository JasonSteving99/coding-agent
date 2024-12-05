"""Tests for the page number ordering function.

This test suite validates a function that takes a comma-separated string of page numbers
and returns a new comma-separated string with the numbers reordered according to specific rules.

Key test aspects covered:
- Input string contains varying numbers of page numbers (3-5 numbers)
- Input numbers are all positive integers
- Output maintains comma-separated format without spaces
- Numbers in output are ordered based on specific business rules from part 1
- Function preserves all input numbers in output (no numbers lost/added)
"""

from solution import order_page_numbers
import pytest

def test_five_numbers_ordering():
    """Test ordering of five page numbers."""
    input_str = "75,97,47,61,53"
    expected = "97,75,47,61,53"
    result = order_page_numbers(input_str)
    assert result == expected, \
        f"For input '{input_str}' expected '{expected}' but got '{result}'"

def test_three_numbers_ordering():
    """Test ordering of three page numbers."""
    input_str = "61,13,29"
    expected = "61,29,13"
    result = order_page_numbers(input_str)
    assert result == expected, \
        f"For input '{input_str}' expected '{expected}' but got '{result}'"

def test_five_numbers_different_order():
    """Test ordering of five different page numbers."""
    input_str = "97,13,75,29,47"
    expected = "97,75,47,29,13"
    result = order_page_numbers(input_str)
    assert result == expected, \
        f"For input '{input_str}' expected '{expected}' but got '{result}'"

def test_result_format():
    """Test that the output maintains correct format (no spaces, comma separated)."""
    input_str = "75,97,47,61,53"
    result = order_page_numbers(input_str)
    assert all(char.isdigit() or char == ',' for char in result), \
        f"Output '{result}' contains invalid characters (only digits and commas allowed)"
    assert not result.startswith(',') and not result.endswith(','), \
        f"Output '{result}' should not start or end with a comma"
    assert ' ' not in result, \
        f"Output '{result}' should not contain spaces"

def test_number_preservation():
    """Test that all input numbers are preserved in the output."""
    input_str = "75,97,47,61,53"
    result = order_page_numbers(input_str)
    input_numbers = set(map(int, input_str.split(',')))
    output_numbers = set(map(int, result.split(',')))
    assert input_numbers == output_numbers, \
        f"Numbers in output '{result}' don't match input numbers '{input_str}'"