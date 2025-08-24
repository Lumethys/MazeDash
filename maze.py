"""
Maze class for generating and managing the game maze.
"""

import pygame
import constants
from maze_generator import MazeGenerator

class Maze:
    def __init__(self, generator: MazeGenerator):
        """Initialize the maze with a predefined layout."""
        # Simple maze layout (1 = wall, 0 = path, 2 = start, 3 = end)
        self.grid = generator.generate()
        
        # Find start and end positions
        start_pos = None
        end_pos = None
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == constants.START:
                    start_pos = (x, y)
                elif self.grid[y][x] == constants.END:
                    end_pos = (x, y)

        if start_pos is None or end_pos is None:
            raise ValueError("Maze must have a start and end position.")

        self.start_pos: tuple[int, int] = start_pos
        self.end_pos: tuple[int, int] = end_pos
    
    def get_start_position(self) -> tuple[int, int]:
        """Return the start position as (x, y) coordinates."""
        return self.start_pos
    
    def get_end_position(self) -> tuple[int, int]:
        """Return the end position as (x, y) coordinates."""
        return self.end_pos
    
    def is_wall(self, x, y):
        """Check if the given position is a wall."""
        if x < 0 or x >= constants.MAZE_WIDTH or y < 0 or y >= constants.MAZE_HEIGHT:
            return True
        return self.grid[y][x] == constants.WALL
    
    def is_end(self, x, y):
        """Check if the given position is the end."""
        if x < 0 or x >= constants.MAZE_WIDTH or y < 0 or y >= constants.MAZE_HEIGHT:
            return False
        return self.grid[y][x] == constants.END
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """Draw the maze on the screen."""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                rect = pygame.Rect(x * constants.CELL_SIZE + offset_x, 
                                 y * constants.CELL_SIZE + offset_y, 
                                   constants.CELL_SIZE, constants.CELL_SIZE)
                
                cell_type = self.grid[y][x]
                
                if cell_type == constants.WALL:
                    pygame.draw.rect(screen, constants.DARK_GRAY, rect)
                    pygame.draw.rect(screen, constants.BLACK, rect, 1)
                elif cell_type == constants.PATH:
                    pygame.draw.rect(screen, constants.WHITE, rect)
                    pygame.draw.rect(screen, constants.LIGHT_GRAY, rect, 1)
                elif cell_type == constants.START:
                    pygame.draw.rect(screen, constants.GREEN, rect)
                    pygame.draw.rect(screen, constants.BLACK, rect, 2)
                elif cell_type == constants.END:
                    pygame.draw.rect(screen, constants.RED, rect)
                    pygame.draw.rect(screen, constants.BLACK, rect, 2)
