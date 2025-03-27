# Blob Simulation

This repository implements a simulation of autonomous "blobs" that interact, form colonies, and move within a hexagonal grid. The simulation is built using Python and Pygame.

---

## Features

- **Blob Behavior**: Each blob has unique traits like sociability, territoriality, loyalty, and boldness, influencing its decisions and interactions.
- **Colony Formation**: Blobs can form colonies based on compatibility and manage their territory dynamically.
- **Pathfinding and Movement**: Blobs navigate the grid using pathfinding algorithms, avoiding occupied cells.
- **Interactive Simulation**: Visualize blob behaviors and colony dynamics in real-time.

---

## Key Components

### 1. **Blob Behavior**
Defined in [`core/blob_behavior`](core/blob_behavior), this module handles:
- Decision-making using Markov processes.
- Interaction logic, including conversations and colony formation.
- Pathfinding and movement.

### 2. **Colony Management**
Implemented in [`core/colony.py`](core/colony.py), colonies:
- Claim and expand territory.
- Assign roles to member blobs (e.g., Worker, Defender).
- Spawn new blobs periodically.

### 3. **Grid Utilities**
The [`core/grid.py`](core/grid.py) module provides:
- Hexagonal grid calculations.
- Neighbor detection for interaction logic.

### 4. **UI Panels**
The [`ui/panels.py`](ui/panels.py) module renders:
- Blob decision-making and personality traits.
- Colony and territory details.

---

## How It Works

1. **Initialization**: The simulation initializes blobs and the grid.
2. **Update Loop**: Each simulation tick:
   - Blobs update their state, interact, and move.
   - Colonies manage their members and territory.
3. **Rendering**: The grid, blobs, and UI panels are drawn using Pygame.

---

## Running the Simulation

1. Install dependencies:
   ```bash
   pip install pygame