"""
Game state classes for managing different screens and states.
"""

import pygame
import sys
from constants import *
from maze import Maze
from player import Player

class GameState:
    """Base class for all game states."""
    
    def __init__(self, game):
        self.game = game
    
    def handle_event(self, event):
        """Handle pygame events."""
        pass
    
    def update(self):
        """Update game state logic."""
        pass
    
    def draw(self, screen):
        """Draw the game state."""
        pass

class MenuState(GameState):
    """Main menu state."""
    
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.title_text = self.font_large.render("Maze Game", True, WHITE)
        self.start_text = self.font_medium.render("Press SPACE to Start", True, WHITE)
        self.quit_text = self.font_medium.render("Press ESC to Quit", True, WHITE)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state(STATE_GAME)
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw title
        title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(self.title_text, title_rect)
        
        # Draw start instruction
        start_rect = self.start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(self.start_text, start_rect)
        
        # Draw quit instruction
        quit_rect = self.quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(self.quit_text, quit_rect)

class GamePlayState(GameState):
    """Main gameplay state."""
    
    def __init__(self, game):
        super().__init__(game)
        self.maze = Maze()
        start_x, start_y = self.maze.get_start_position()
        self.player = Player(start_x, start_y)
        self.font = pygame.font.Font(None, 36)
        
        # Calculate maze offset to center it on screen
        maze_pixel_width = MAZE_WIDTH * CELL_SIZE
        maze_pixel_height = MAZE_HEIGHT * CELL_SIZE
        self.maze_offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        self.maze_offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state(STATE_MENU)
            elif event.key in [pygame.K_UP, pygame.K_w]:
                self.player.move(0, -1, self.maze)
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.player.move(0, 1, self.maze)
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                self.player.move(-1, 0, self.maze)
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.player.move(1, 0, self.maze)
    
    def update(self):
        self.player.update()
        
        # Check if player reached the end
        if self.maze.is_end(self.player.grid_x, self.player.grid_y):
            self.game.change_state(STATE_POPUP)
    
    def draw(self, screen):
        screen.fill(GRAY)
        
        # Draw maze
        self.maze.draw(screen, self.maze_offset_x, self.maze_offset_y)
        
        # Draw player
        self.player.draw(screen, self.maze_offset_x, self.maze_offset_y)
        
        # Draw instructions
        instructions = [
            "Use Arrow Keys or WASD to move",
            "Reach the red square to win!",
            "Press ESC to return to menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 24).render(instruction, True, WHITE)
            screen.blit(text, (10, 10 + i * 25))

class PopupState(GameState):
    """Congratulations popup state."""
    
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.congrats_text = self.font_large.render("Congratulations!", True, WHITE)
        self.complete_text = self.font_medium.render("You completed the maze!", True, WHITE)
        self.return_text = self.font_medium.render("Press SPACE to return to main menu", True, WHITE)
        
        # Create popup rectangle
        self.popup_width = 500
        self.popup_height = 300
        self.popup_x = (SCREEN_WIDTH - self.popup_width) // 2
        self.popup_y = (SCREEN_HEIGHT - self.popup_height) // 2
        self.popup_rect = pygame.Rect(self.popup_x, self.popup_y, self.popup_width, self.popup_height)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state(STATE_MENU)
    
    def draw(self, screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw popup background
        pygame.draw.rect(screen, DARK_GRAY, self.popup_rect)
        pygame.draw.rect(screen, WHITE, self.popup_rect, 3)
        
        # Draw congratulations text
        congrats_rect = self.congrats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(self.congrats_text, congrats_rect)
        
        # Draw completion text
        complete_rect = self.complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
        screen.blit(self.complete_text, complete_rect)
        
        # Draw return instruction
        return_rect = self.return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(self.return_text, return_rect)

class Game:
    """Main game class that manages all states."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Maze Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize states
        self.states = {
            STATE_MENU: MenuState(self),
            STATE_GAME: GamePlayState(self),
            STATE_POPUP: PopupState(self)
        }
        
        self.current_state = STATE_MENU
    
    def change_state(self, new_state):
        """Change the current game state."""
        if new_state == STATE_GAME:
            # Reset the game state when starting a new game
            self.states[STATE_GAME] = GamePlayState(self)
        
        self.current_state = new_state
    
    def quit(self):
        """Quit the game."""
        self.running = False
    
    def run(self):
        """Main game loop."""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.states[self.current_state].handle_event(event)
            
            # Update current state
            self.states[self.current_state].update()
            
            # Draw current state
            self.states[self.current_state].draw(self.screen)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
