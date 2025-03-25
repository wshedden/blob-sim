import math

# --- Hex Grid Constants ---
HEX_RADIUS = 20
HEX_WIDTH = math.sqrt(3) * HEX_RADIUS     # ≈ 34.64
HEX_HEIGHT = 2 * HEX_RADIUS               # = 40
VERTICAL_SPACING = 0.75 * HEX_HEIGHT      # = 30

GRID_COLS = 15
GRID_ROWS = 15

# --- UI Layout ---
PANEL_WIDTH = 240
MARGIN = 50  # Margin around grid (used for placement calculations)

# Derived grid size (pixel dimensions)
GRID_PIXEL_WIDTH = int(HEX_WIDTH * (GRID_COLS + 0.5))
GRID_PIXEL_HEIGHT = int(HEX_HEIGHT * 0.75 * (GRID_ROWS - 1) + HEX_HEIGHT)

WINDOW_WIDTH = GRID_PIXEL_WIDTH + 2 * PANEL_WIDTH + 2 * MARGIN
WINDOW_HEIGHT = GRID_PIXEL_HEIGHT + 2 * MARGIN

# --- Behaviour ---
FPS = 60
MOVE_DURATION = FPS  # 60 frames = 1 second per cell move

# --- Colours ---
BG_COLOR = (245, 245, 255)
HEX_COLOR = (220, 220, 220)
GRID_LINE_COLOR = (100, 100, 100)
EYE_COLOR = (0, 0, 0)

PANEL_BG = (50, 50, 80)
DETAIL_PANEL_BG = (30, 30, 60)
TEXT_COLOR = (255, 255, 255)

# --- Rendering ---
TARGET_OUTLINE_WIDTH = 3
