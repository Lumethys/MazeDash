"""
Maze class for generating and managing the game maze.
"""

import pygame
from constants import *

class Maze:
    def __init__(self):
        """Initialize the maze with a predefined layout."""
        # Simple maze layout (1 = wall, 0 = path, 2 = start, 3 = end)
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Find start and end positions
        self.start_pos = None
        self.end_pos = None
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == START:
                    self.start_pos = (x, y)
                elif self.grid[y][x] == END:
                    self.end_pos = (x, y)
    
    def get_start_position(self):
        """Return the start position as (x, y) coordinates."""
        return self.start_pos
    
    def get_end_position(self):
        """Return the end position as (x, y) coordinates."""
        return self.end_pos
    
    def is_wall(self, x, y):
        """Check if the given position is a wall."""
        if x < 0 or x >= MAZE_WIDTH or y < 0 or y >= MAZE_HEIGHT:
            return True
        return self.grid[y][x] == WALL
    
    def is_end(self, x, y):
        """Check if the given position is the end."""
        if x < 0 or x >= MAZE_WIDTH or y < 0 or y >= MAZE_HEIGHT:
            return False
        return self.grid[y][x] == END
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """Draw the maze on the screen."""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                rect = pygame.Rect(x * CELL_SIZE + offset_x, 
                                 y * CELL_SIZE + offset_y, 
                                 CELL_SIZE, CELL_SIZE)
                
                cell_type = self.grid[y][x]
                
                if cell_type == WALL:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                elif cell_type == PATH:
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)
                elif cell_type == START:
                    pygame.draw.rect(screen, GREEN, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)
                elif cell_type == END:
                    pygame.draw.rect(screen, RED, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)
