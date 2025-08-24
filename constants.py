"""
Constants for the maze game application.
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Maze settings
MAZE_WIDTH = 15
MAZE_HEIGHT = 11
CELL_SIZE = 40

# Game states
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_POPUP = "popup"
STATE_QUIT = "quit"

# Maze cell types
WALL = 1
PATH = 0
START = 2
END = 3

# Player movement speed (pixels per frame)
PLAYER_SPEED = 2
