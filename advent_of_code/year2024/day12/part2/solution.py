from typing import List, Set, Dict, Tuple
from collections import deque

def get_regions(grid: List[List[str]]) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    height = len(grid)
    width = len(grid[0])
    visited = set()
    regions = {}
    
    def get_neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < height and 0 <= nc < width and 
                grid[nr][nc] == grid[r][c]):
                neighbors.append((nr, nc))
        return neighbors
    
    for r in range(height):
        for c in range(width):
            if (r, c) not in visited:
                plant = grid[r][c]
                region = []
                queue = deque([(r, c)])
                visited.add((r, c))
                
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region.append((curr_r, curr_c))
                    
                    for nr, nc in get_neighbors(curr_r, curr_c):
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                
                for pos in region:
                    regions[pos] = region
                    
    return regions

def count_region_sides(region: List[Tuple[int, int]], grid: List[List[str]]) -> int:
    height = len(grid)
    width = len(grid[0])
    region_set = set(region)
    
    # Track edges between cells
    edges = set()
    
    for r, c in region:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            # If neighbor is outside grid or not in region, it's a boundary
            if (nr < 0 or nr >= height or nc < 0 or nc >= width or 
                (nr, nc) not in region_set):
                # Create a unique identifier for this edge
                if dr == 0:  # Vertical edge
                    edge = ((r, min(c, nc)), (r + 1, min(c, nc)))
                else:  # Horizontal edge
                    edge = ((min(r, nr), c), (min(r, nr), c + 1))
                
                edges.add(edge)
    
    return len(edges)

def calculate_total_price_with_bulk_discount(input_str: str) -> int:
    # Convert input string to grid
    grid = [list(line) for line in input_str.strip().split('\n')]
    
    # Get all regions
    regions = get_regions(grid)
    
    # Calculate total price
    total_price = 0
    processed_regions = set()
    
    for pos in regions:
        region = regions[pos]
        # Convert to tuple for hashing
        region_tuple = tuple(sorted(region))
        
        if region_tuple not in processed_regions:
            area = len(region)
            num_sides = count_region_sides(region, grid)
            price = area * num_sides
            total_price += price
            processed_regions.add(region_tuple)
    
    return total_price

def solution() -> int:
    # Read input from stdin
    import sys
    input_data = sys.stdin.read().strip()
    return calculate_total_price_with_bulk_discount(input_data)