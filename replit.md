# Overview

A simple 2D maze game built with Pygame where players navigate through a predefined maze using keyboard controls (arrow keys or WASD) to reach the end goal. The game features a state-based architecture with menu and gameplay screens, smooth player movement animations, and collision detection with maze walls.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Game Architecture Pattern
The application follows a state machine pattern with distinct game states (menu, gameplay, popup) managed through a central Game class. This approach provides clear separation of concerns and makes it easy to add new screens or game modes.

## Core Components

**Game State Management**: Uses inheritance-based state classes (GameState, MenuState) to handle different screens and game phases. Each state manages its own event handling, update logic, and rendering.

**Entity System**: Simple object-oriented approach with separate classes for game entities (Player, Maze). The Player class handles position tracking, movement validation, and smooth animation between grid positions.

**Maze System**: Static maze layout defined as a 2D array with different cell types (walls, paths, start, end positions). The maze provides collision detection and position validation services to other game components.

**Rendering System**: Direct Pygame rendering with a coordinate system that maps grid positions to pixel coordinates. Uses CELL_SIZE constant to scale the maze appropriately for the screen resolution.

## Movement and Animation
The player movement system uses a grid-based approach with smooth pixel-level animations. Players move between discrete grid positions, but the visual representation animates smoothly using interpolation between current and target positions.

## Constants Management
All game configuration (screen dimensions, colors, speeds, maze settings) is centralized in a constants module, making the game easily configurable and maintainable.

# External Dependencies

**Pygame**: Core game engine providing window management, event handling, graphics rendering, and input processing. Handles all low-level game functionality including the main game loop, sprite rendering, and cross-platform compatibility.

**Python Standard Library**: Uses `sys` for program termination and path management, and `os` for file path operations during module imports.