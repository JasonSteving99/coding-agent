from typing import Optional, List, Tuple
import sys
from dataclasses import dataclass
import re
from math import gcd


@dataclass
class ClawMachine:
    button_a: Tuple[int, int]  # (x, y) movement for button A
    button_b: Tuple[int, int]  # (x, y) movement for button B
    prize: Tuple[int, int]     # (x, y) coordinates of prize


def parse_machine(lines: List[str]) -> ClawMachine:
    """Parse a single claw machine configuration from input lines."""
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    match = re.match(pattern, "\n".join(lines))
    if not match:
        raise ValueError("Invalid input format")
    
    nums = [int(x) for x in match.groups()]
    return ClawMachine(
        button_a=(nums[0], nums[1]),
        button_b=(nums[2], nums[3]),
        prize=(nums[4], nums[5])
    )


def bezout_coefficients(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Returns (gcd, x, y) where gcd is the greatest common divisor of a and b
    and x, y are coefficients where ax + by = gcd
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def solve_machine_diophantine(machine: ClawMachine) -> Optional[Tuple[int, int]]:
    """
    Solve the system of Diophantine equations for the machine using the extended Euclidean algorithm.
    Returns (a_presses, b_presses) or None if no solution exists.
    """
    # For X coordinates: a₁x + b₁y = target_x
    # For Y coordinates: a₂x + b₂y = target_y
    a1, b1 = machine.button_a[0], machine.button_b[0]  # x-movements
    a2, b2 = machine.button_a[1], machine.button_b[1]  # y-movements
    target_x, target_y = machine.prize

    # First equation: a₁x + b₁y = target_x
    gcd_x, x1, y1 = bezout_coefficients(a1, b1)
    if target_x % gcd_x != 0:
        return None

    # Second equation: a₂x + b₂y = target_y
    gcd_y, x2, y2 = bezout_coefficients(a2, b2)
    if target_y % gcd_y != 0:
        return None

    # Particular solutions
    x1 = x1 * (target_x // gcd_x)
    y1 = y1 * (target_x // gcd_x)
    x2 = x2 * (target_y // gcd_y)
    y2 = y2 * (target_y // gcd_y)

    # Find k where both solutions align (we need positive solutions)
    k1_start = max((-x1 * gcd_x) // (b1), (-y1 * gcd_x) // (-a1))
    k2_start = max((-x2 * gcd_y) // (b2), (-y2 * gcd_y) // (-a2))

    # Try some reasonable number of k values
    for k1 in range(k1_start, k1_start + 1000):
        a_press1 = x1 + (b1 // gcd_x) * k1
        b_press1 = y1 - (a1 // gcd_x) * k1
        
        for k2 in range(k2_start, k2_start + 1000):
            a_press2 = x2 + (b2 // gcd_y) * k2
            b_press2 = y2 - (a2 // gcd_y) * k2
            
            if a_press1 == a_press2 and b_press1 == b_press2 and a_press1 >= 0 and b_press1 >= 0:
                return (a_press1, b_press1)

    return None


def solve_machine(machine: ClawMachine) -> Optional[int]:
    """
    Solve for a single machine, returning minimum tokens needed or None if unsolvable.
    A button costs 3 tokens, B button costs 1 token.
    """
    solution = solve_machine_diophantine(machine)
    if solution is not None:
        a_presses, b_presses = solution
        return 3 * a_presses + b_presses
    return None


def calculate_min_tokens_part2(input_str: str) -> int:
    """Calculate minimum tokens needed for part 2 with modified prize coordinates."""
    machines_str = [m.strip() for m in input_str.strip().split("\n\n")]
    total_tokens = 0
    prizes_possible = False
    offset = 10000000000000

    for machine_str in machines_str:
        lines = machine_str.split("\n")
        machine = parse_machine(lines)
        # Modify prize coordinates
        machine.prize = (machine.prize[0] + offset, machine.prize[1] + offset)
        solution = solve_machine(machine)
        
        if solution is not None:
            prizes_possible = True
            total_tokens += solution
    
    if not prizes_possible:
        return 0
    return total_tokens


def solution() -> int:
    """Read from stdin and return the solution."""
    input_str = sys.stdin.read()
    return calculate_min_tokens_part2(input_str)