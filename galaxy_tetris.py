import pygame
import sys
import random

# --- Game Window Setup ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30
PLAY_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
PLAY_Y = SCREEN_HEIGHT - PLAY_HEIGHT

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)

SHAPE_COLORS = [
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (128, 0, 128),  # T
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (0, 0, 255),    # J
    (255, 165, 0),  # L
]

# --- Tetris Shapes ---
SHAPES = [
    [[1, 1, 1, 1]],                      # I
    [[1, 1], [1, 1]],                    # O
    [[0, 1, 0], [1, 1, 1]],             # T
    [[0, 1, 1], [1, 1, 0]],             # S
    [[1, 1, 0], [0, 1, 1]],             # Z
    [[1, 0, 0], [1, 1, 1]],             # J
    [[0, 0, 1], [1, 1, 1]],             # L
]

# --- Helper Functions ---
def rotate_shape(shape):
    """Rotate the shape clockwise."""
    return [list(row) for row in zip(*shape[::-1])]

# --- Piece Class ---
class Piece:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def rotate(self):
        self.shape = rotate_shape(self.shape)

# --- Game State ---
class GameState:
    def __init__(self):
        self.grid = [[BLACK for _ in range(10)] for _ in range(20)]
        self.current_piece = self._get_new_piece()
        self.next_piece = self._get_new_piece()
        self.score = 0
        self.game_over = False

    def _get_new_piece(self):
        idx = random.randint(0, len(SHAPES) - 1)
        template = SHAPES[idx]
        spawn_x = (10 - len(template[0])) // 2
        return Piece(spawn_x, -len(template), template, SHAPE_COLORS[idx])

# --- Tetris Game ---
class TetrisGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.joystick.init()

        # Load sounds
        self.sounds = {
            "background": pygame.mixer.Sound("bgsound.mp3"),
            "rotate": pygame.mixer.Sound("explosion.mp3"),
            "drop": pygame.mixer.Sound("explosion.mp3"),
            "clear": pygame.mixer.Sound("clear.mp3"),
            "game_over": pygame.mixer.Sound("gameover.mp3"),
        }
        self.sounds["background"].play(-1)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PyTetris 🎮")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("comicsans", 30)
        self.game_state = GameState()
        self.fall_time = 0
        self.fall_speed = 0.5
        self.running = True

        # --- Joystick Setup ---
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"🎮 Joystick detected: {self.joystick.get_name()}")
        else:
            print("⚠️ No joystick detected. Using keyboard controls instead.")

    # --- Grid Drawing ---
    def _draw_grid(self):
        for y in range(20):
            for x in range(10):
                pygame.draw.rect(
                    self.screen,
                    self.game_state.grid[y][x],
                    (PLAY_X + x * BLOCK_SIZE, PLAY_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0
                )
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    (PLAY_X + x * BLOCK_SIZE, PLAY_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )

    def _draw_next_piece(self):
        label = self.font.render("Next Piece", True, WHITE)
        self.screen.blit(label, (SCREEN_WIDTH - 200, 100))
        piece = self.game_state.next_piece
        for y, row in enumerate(piece.shape):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        piece.color,
                        (SCREEN_WIDTH - 200 + x * BLOCK_SIZE, 150 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        0
                    )

    def _valid_space(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                if val:
                    new_x = self.game_state.current_piece.x + x + offset_x
                    new_y = self.game_state.current_piece.y + y + offset_y
                    if new_x < 0 or new_x >= 10 or new_y >= 20:
                        return False
                    if new_y >= 0 and self.game_state.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def _lock_piece(self):
        piece = self.game_state.current_piece
        for y, row in enumerate(piece.shape):
            for x, val in enumerate(row):
                if val:
                    if piece.y + y < 0:
                        self.sounds["game_over"].play()
                        self.game_state.game_over = True
                        return
                    self.game_state.grid[piece.y + y][piece.x + x] = piece.color
        self.game_state.current_piece = self.game_state.next_piece
        self.game_state.next_piece = self.game_state._get_new_piece()
        self._clear_lines()

    def _clear_lines(self):
        lines_cleared = 0
        for y in range(19, -1, -1):
            if BLACK not in self.game_state.grid[y]:
                del self.game_state.grid[y]
                self.game_state.grid.insert(0, [BLACK for _ in range(10)])
                lines_cleared += 1
        if lines_cleared > 0:
            self.sounds["clear"].play()
        self.game_state.score += lines_cleared * 100

    def _draw_window(self):
        self.screen.fill(BLACK)
        self._draw_grid()

        piece = self.game_state.current_piece
        for y, row in enumerate(piece.shape):
            for x, val in enumerate(row):
                if val:
                    draw_x = PLAY_X + (piece.x + x) * BLOCK_SIZE
                    draw_y = PLAY_Y + (piece.y + y) * BLOCK_SIZE
                    if draw_y >= PLAY_Y:
                        pygame.draw.rect(self.screen, piece.color, (draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE), 0)

        self._draw_next_piece()
        score_label = self.font.render(f"Score: {self.game_state.score}", True, WHITE)
        self.screen.blit(score_label, (SCREEN_WIDTH - 200, 300))

        if self.game_state.game_over:
            label = self.font.render("GAME OVER! Press Start to Restart", True, (255, 0, 0))
            self.screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.update()

    def reset_game(self):
        self.game_state = GameState()
        self.fall_time = 0
        self.fall_speed = 0.5

    def run(self):
        while self.running:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()
            if self.fall_time / 1000 >= self.fall_speed:
                self.fall_time = 0
                if self._valid_space(self.game_state.current_piece.shape, 0, 1):
                    self.game_state.current_piece.y += 1
                else:
                    self._lock_piece()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # 🎮 Joystick Controls
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1:  # X / A → Rotate
                        rotated = rotate_shape(self.game_state.current_piece.shape)
                        if self._valid_space(rotated, 0, 0):
                            self.game_state.current_piece.shape = rotated
                            self.sounds["rotate"].play()
                    elif event.button == 2:  # O / B → Hard Drop
                        while self._valid_space(self.game_state.current_piece.shape, 0, 1):
                            self.game_state.current_piece.y += 1
                        self.sounds["drop"].play()
                        self._lock_piece()
                    elif event.button == 7:  # Start Button → Restart
                        if self.game_state.game_over:
                            self.reset_game()

                if event.type == pygame.JOYAXISMOTION:
                    # Left joystick or D-Pad
                    x_axis = self.joystick.get_axis(0)
                    y_axis = self.joystick.get_axis(1)

                    if x_axis < -0.5:  # Left
                        if self._valid_space(self.game_state.current_piece.shape, -1, 0):
                            self.game_state.current_piece.x -= 1
                    elif x_axis > 0.5:  # Right
                        if self._valid_space(self.game_state.current_piece.shape, 1, 0):
                            self.game_state.current_piece.x += 1
                    if y_axis > 0.5:  # Soft Drop
                        if self._valid_space(self.game_state.current_piece.shape, 0, 1):
                            self.game_state.current_piece.y += 1
                        else:
                            self._lock_piece()

            self._draw_window()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()
