"""
This test suite covers the count_visited_positions function which:
1. Takes a string input representing a 10x10 grid map with:
   - '.' for empty spaces
   - '#' for obstacles
   - '^' for guard's starting position facing up
2. Returns an integer representing the number of distinct positions visited
   by the guard before exiting the map boundaries following a movement protocol
"""

from solution import count_visited_positions
import pytest

def test_guard_movement_with_obstacles():
    # Test case with guard starting at bottom half of grid facing up
    input_grid = (
        "....#.....\n"
        ".........#\n"
        "..........\n"
        "..#.......\n"
        ".......#..\n"
        "..........\n"
        ".#..^.....\n"
        "........#.\n"
        "#.........\n"
        "......#..."
    )
    expected_positions = 41
    
    result = count_visited_positions(input_grid)
    
    assert result == expected_positions, \
        f"Guard should visit {expected_positions} distinct positions before exiting the map.\n" \
        f"Input grid:\n{input_grid}\n" \
        f"Got {result} positions instead."


def test_input_validation():
    # Test with empty input
    assert count_visited_positions("") == 0

    # Test with missing guard position
    input_grid = ("." * 10 + "\n") * 10
    assert count_visited_positions(input_grid.strip()) == 0