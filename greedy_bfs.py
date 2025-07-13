import pygame
import heapq
import time  

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Greedy Best-First Search Visualization")

# Grid setup
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start = None
end = None
path_found = False

def heuristic(a, b):
    """Heuristic function for Manhattan distance."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def draw_grid():
    """Draw the grid lines."""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_cells():
    """Draw the cells of the grid."""
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * GRID_SIZE, row * GRID_SIZE
            if grid[row][col] == 1:  # Wall
                pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE))
            elif (row, col) == start:  # Start
                pygame.draw.rect(screen, GREEN, (x, y, GRID_SIZE, GRID_SIZE))
            elif (row, col) == end:  # End
                pygame.draw.rect(screen, RED, (x, y, GRID_SIZE, GRID_SIZE))
            elif grid[row][col] == 2:  # Path
                pygame.draw.rect(screen, YELLOW, (x, y, GRID_SIZE, GRID_SIZE))
            elif grid[row][col] == 3:  # Visited
                pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))

def gbfs(start, end):
    """Greedy Best-First Search algorithm."""
    global path_found
    open_set = []
    heapq.heappush(open_set, (heuristic(start, end), start))
    came_from = {}
    visited = set()
    
    start_time = time.perf_counter()  # Start timing

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            end_time = time.perf_counter()  # End timing
            reconstruct_path(came_from, start, end)
            path_found = True
            print(f"Path found! Total time: {end_time - start_time:.6f} seconds")
            print(f"Path distance: {calculate_path_distance(came_from, start, end)} steps")
            return

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Four possible movements
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and grid[neighbor[0]][neighbor[1]] != 1:
                if neighbor not in visited:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (heuristic(neighbor, end), neighbor))
                    grid[neighbor[0]][neighbor[1]] = 3  # Mark as visited

    end_time = time.perf_counter()
    print(f"No path found. Total time: {end_time - start_time:.6f} seconds")

def reconstruct_path(came_from, start, end):
    """Reconstruct the path from start to end."""
    current = end
    while current != start:
        grid[current[0]][current[1]] = 2  # Mark as part of the path
        current = came_from[current]

def calculate_path_distance(came_from, start, end):
    """Calculate the path distance (number of steps)."""
    distance = 0
    current = end
    while current != start:
        current = came_from.get(current)
        if current is None:
            return 0  # No valid path
        distance += 1
    return distance

# Main loop
running = True
placing_walls = False
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_cells()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = y // GRID_SIZE, x // GRID_SIZE
            if event.button == 1:  # Left click
                if not start:
                    start = (row, col)
                elif not end:
                    end = (row, col)
                else:
                    placing_walls = True
            elif event.button == 3:  # Right click to remove walls
                grid[row][col] = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                placing_walls = False
        elif event.type == pygame.MOUSEMOTION:
            if placing_walls:
                x, y = pygame.mouse.get_pos()
                row, col = y // GRID_SIZE, x // GRID_SIZE
                if (row, col) != start and (row, col) != end:
                    grid[row][col] = 1  # Mark as wall
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:  # Run GBFS
                grid = [[0 if cell != 1 else 1 for cell in row] for row in grid]
                gbfs(start, end)

    pygame.display.flip()

pygame.quit()
