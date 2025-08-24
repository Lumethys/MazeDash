"""
Game state classes for managing different screens and states.
"""

from typing import Callable
import pygame
import constants
from maze import Maze
from maze_generator import MazeGenerator
from player import Player


class GameState:
    """Base class for all game states."""

    def __init__(self, change_state: Callable[[str], None]) -> None:
        self.change_state = change_state

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

    def __init__(self, change_state: Callable[[str], None]) -> None:
        super().__init__(change_state)
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.title_text = self.font_large.render("Maze Game", True,
                                                 constants.WHITE)
        self.start_text = self.font_medium.render("Press SPACE to Start", True,
                                                  constants.WHITE)
        self.quit_text = self.font_medium.render("Press ESC to Quit", True,
                                                 constants.WHITE)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.change_state(constants.STATE_GAME)
            elif event.key == pygame.K_ESCAPE:
                self.change_state(constants.STATE_QUIT)

    def draw(self, screen):
        screen.fill(constants.BLACK)

        # Draw title
        title_rect = self.title_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 - 100))
        screen.blit(self.title_text, title_rect)

        # Draw start instruction
        start_rect = self.start_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2))
        screen.blit(self.start_text, start_rect)

        # Draw quit instruction
        quit_rect = self.quit_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 + 60))
        screen.blit(self.quit_text, quit_rect)


class GamePlayState(GameState):
    """Main gameplay state."""

    def __init__(self, change_state: Callable[[str], None]) -> None:
        super().__init__(change_state)
        maze_generator: MazeGenerator = MazeGenerator(
            constants.MAZE_WIDTH, constants.MAZE_HEIGHT, lambda w, h:
            (w + h) // 4)
        self.maze = Maze(maze_generator)
        start_x, start_y = self.maze.get_start_position()
        self.player = Player(start_x, start_y)
        self.font = pygame.font.Font(None, 36)

        # Calculate maze offset to center it on screen
        maze_pixel_width = constants.MAZE_WIDTH * constants.CELL_SIZE
        maze_pixel_height = constants.MAZE_HEIGHT * constants.CELL_SIZE
        self.maze_offset_x = (constants.SCREEN_WIDTH - maze_pixel_width) // 2
        self.maze_offset_y = (constants.SCREEN_HEIGHT - maze_pixel_height) // 2

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.change_state(constants.STATE_MENU)
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
            self.change_state(constants.STATE_POPUP)

    def draw(self, screen):
        screen.fill(constants.GRAY)

        # Draw maze
        self.maze.draw(screen, self.maze_offset_x, self.maze_offset_y)

        # Draw player
        self.player.draw(screen, self.maze_offset_x, self.maze_offset_y)

        # Draw instructions
        instructions = [
            "Use Arrow Keys or WASD to move", "Reach the red square to win!",
            "Press ESC to return to menu"
        ]

        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 24).render(instruction, True,
                                                     constants.WHITE)
            screen.blit(text, (10, 10 + i * 25))


class PopupState(GameState):
    """Congratulations popup state."""

    def __init__(self, change_state: Callable[[str], None]) -> None:
        super().__init__(change_state)
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.congrats_text = self.font_large.render("Congratulations!", True,
                                                    constants.WHITE)
        self.complete_text = self.font_medium.render("You completed the maze!",
                                                     True, constants.WHITE)
        self.return_text = self.font_medium.render(
            "Press SPACE to return to main menu", True, constants.WHITE)

        # Create popup rectangle
        self.popup_width = 500
        self.popup_height = 300
        self.popup_x = (constants.SCREEN_WIDTH - self.popup_width) // 2
        self.popup_y = (constants.SCREEN_HEIGHT - self.popup_height) // 2
        self.popup_rect = pygame.Rect(self.popup_x, self.popup_y,
                                      self.popup_width, self.popup_height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.change_state(constants.STATE_MENU)

    def draw(self, screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(constants.BLACK)
        screen.blit(overlay, (0, 0))

        # Draw popup background
        pygame.draw.rect(screen, constants.DARK_GRAY, self.popup_rect)
        pygame.draw.rect(screen, constants.WHITE, self.popup_rect, 3)

        # Draw congratulations text
        congrats_rect = self.congrats_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 - 60))
        screen.blit(self.congrats_text, congrats_rect)

        # Draw completion text
        complete_rect = self.complete_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 - 10))
        screen.blit(self.complete_text, complete_rect)

        # Draw return instruction
        return_rect = self.return_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 + 40))
        screen.blit(self.return_text, return_rect)
