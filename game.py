import sys
import pygame
import constants
from game_states import MenuState, GamePlayState, PopupState, GameState

class Game:
  """Main game class that manages all states."""

  def __init__(self) -> None:
      pygame.init()
      self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
      pygame.display.set_caption("2D Maze Game")
      self.clock = pygame.time.Clock()
      self.running = True

      # Initialize states
      self.states: dict[str, GameState] = {
          constants.STATE_MENU: MenuState(self.change_state),
          constants.STATE_GAME: GamePlayState(self.change_state),
          constants.STATE_POPUP: PopupState(self.change_state)
      }

      self.current_state = constants.STATE_MENU

  def change_state(self, new_state: str):
      """Change the current game state."""
      if new_state == constants.STATE_QUIT:
          self.quit()
          return
      
      if new_state == constants.STATE_GAME:
          # Reset the game state when starting a new game
          self.states[constants.STATE_GAME] = GamePlayState(self.change_state)

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
          self.clock.tick(constants.FPS)

      pygame.quit()
      sys.exit()