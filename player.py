"""
Player class for the maze game.
"""

import pygame
from constants import *

class Player:
    def __init__(self, x, y):
        """Initialize the player at given grid coordinates."""
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * CELL_SIZE + CELL_SIZE // 2
        self.pixel_y = y * CELL_SIZE + CELL_SIZE // 2
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False
        self.radius = CELL_SIZE // 4
        
    def set_position(self, grid_x, grid_y):
        """Set player position to specific grid coordinates."""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pixel_x = grid_x * CELL_SIZE + CELL_SIZE // 2
        self.pixel_y = grid_y * CELL_SIZE + CELL_SIZE // 2
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False
    
    def move(self, dx, dy, maze):
        """Attempt to move the player by dx, dy grid units."""
        if self.moving:
            return False
            
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        # Check bounds and walls
        if (new_x < 0 or new_x >= MAZE_WIDTH or 
            new_y < 0 or new_y >= MAZE_HEIGHT or
            maze.grid[new_y][new_x] == WALL):
            return False
        
        # Start movement
        self.grid_x = new_x
        self.grid_y = new_y
        self.target_x = new_x * CELL_SIZE + CELL_SIZE // 2
        self.target_y = new_y * CELL_SIZE + CELL_SIZE // 2
        self.moving = True
        return True
    
    def update(self):
        """Update player animation/movement."""
        if self.moving:
            # Move towards target position
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            
            if abs(dx) <= PLAYER_SPEED and abs(dy) <= PLAYER_SPEED:
                # Reached target
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False
            else:
                # Move towards target
                if dx != 0:
                    self.pixel_x += PLAYER_SPEED if dx > 0 else -PLAYER_SPEED
                if dy != 0:
                    self.pixel_y += PLAYER_SPEED if dy > 0 else -PLAYER_SPEED
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """Draw the player on the screen."""
        pygame.draw.circle(screen, BLUE, 
                         (int(self.pixel_x + offset_x), int(self.pixel_y + offset_y)), 
                         self.radius)
        # Add a white outline
        pygame.draw.circle(screen, WHITE, 
                         (int(self.pixel_x + offset_x), int(self.pixel_y + offset_y)), 
                         self.radius, 2)
