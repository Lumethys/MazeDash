"""
Main entry point for the 2D Maze Game.
A simple maze solving game where the player navigates through a maze
using arrow keys or WASD controls to reach the end goal.
"""

import os
import sys

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Game

def main():
    """Main function to start the maze game."""
    try:
        # Create and run the game
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running the game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
