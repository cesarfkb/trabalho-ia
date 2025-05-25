import pygame
import math
import ai

# Board constants
BOARD_SIZE = 500
CENTER = BOARD_SIZE // 2
RADIUS = 200
OUTER_POINTS = 8
PIECE_RADIUS = 30
CENTER_RADIUS = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (220, 220, 220)
BG_COLOR = (245, 245, 245)

class Board:
    def __init__(self, screen=None):
        self.positions = self.calculate_positions()
        self.state = [0]*9
        for i in range(4):
            self.state[i] = 1  # White
        for i in range(4, 8):
            self.state[i] = 2  # Black
        self.selected = None
        self.current_player = 1
        self.first_move_done = False
        self.num_players = None
        self.win_message = None
        self.ai_mode = None
        self.screen = screen
        if self.screen:
            self.show_start_screen()

    def show_start_screen(self):
        font = pygame.font.SysFont(None, 48)
        small_font = pygame.font.SysFont(None, 36)
        choosing = True
        while choosing:
            self.screen.fill(BG_COLOR)
            self.draw_text_center("Choose Game Mode", 100, font)
            pygame.draw.rect(self.screen, (200,200,200), (100,180,300,60))
            self.draw_text_center("1 Player (vs AI)", 210, small_font)
            pygame.draw.rect(self.screen, (200,200,200), (100,270,300,60))
            self.draw_text_center("2 Players", 300, small_font)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if 100 < mx < 400 and 180 < my < 240:
                        self.num_players = 1
                        choosing = False
                        self.show_ai_select_screen()
                        self.show_color_select_screen()
                    elif 100 < mx < 400 and 270 < my < 330:
                        self.num_players = 2
                        choosing = False

    def show_ai_select_screen(self):
        font = pygame.font.SysFont(None, 48)
        small_font = pygame.font.SysFont(None, 36)
        choosing = True
        while choosing:
            self.screen.fill(BG_COLOR)
            self.draw_text_center("Choose AI Mode", 100, font)
            pygame.draw.rect(self.screen, (200,200,200), (100,180,300,60))
            self.draw_text_center("Random AI", 210, small_font)
            pygame.draw.rect(self.screen, (200,200,200), (100,270,300,60))
            self.draw_text_center("Minimax AI", 300, small_font)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if 100 < mx < 400 and 180 < my < 240:
                        self.ai_mode = "random"
                        choosing = False
                    elif 100 < mx < 400 and 270 < my < 330:
                        self.ai_mode = "minimax"
                        choosing = False

    def show_color_select_screen(self):
        font = pygame.font.SysFont(None, 48)
        small_font = pygame.font.SysFont(None, 36)
        choosing = True
        self.player_color = None
        while choosing:
            self.screen.fill(BG_COLOR)
            self.draw_text_center("Choose Your Color", 120, font)
            # Draw White box and text
            pygame.draw.rect(self.screen, (255,255,255), (100,200,120,60))
            self.draw_text_boxed("White", 100, 200, 120, 60, small_font, (0,0,0))
            # Draw Black box and text
            pygame.draw.rect(self.screen, (0,0,0), (280,200,120,60))
            self.draw_text_boxed("Black", 280, 200, 120, 60, small_font, (255,255,255))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if 100 < mx < 220 and 200 < my < 260:
                        self.player_color = 1
                        choosing = False
                    elif 280 < mx < 400 and 200 < my < 260:
                        self.player_color = 2
                        choosing = False
        # After color selection, if AI is white, make the first move
        if self.num_players == 1 and self.player_color == 2:
            # Player is black, AI is white and should move first
            self.ai_move()

    def draw_text_boxed(self, text, x, y, w, h, font, color):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x + w//2, y + h//2))
        self.screen.blit(surf, rect)

    def draw_text_center(self, text, y, font, color=(0,0,0)):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(CENTER, y))
        self.screen.blit(surf, rect)

    def calculate_positions(self):
        positions = []
        for i in range(OUTER_POINTS):
            angle = 2 * math.pi * i / OUTER_POINTS - math.pi / 8
            x = CENTER + RADIUS * math.cos(angle)
            y = CENTER + RADIUS * math.sin(angle)
            positions.append((int(x), int(y)))
        positions.append((CENTER, CENTER))  # Center point
        return positions

    def draw(self, screen):
        screen.fill(BG_COLOR)
        # Draw turn text
        font = pygame.font.SysFont(None, 36)
        turn_text = "White's Turn" if self.current_player == 1 else "Black's Turn"
        text_color = (0,0,0) if self.current_player == 1 else (0,0,0)
        text_surf = font.render(turn_text, True, text_color)
        text_rect = text_surf.get_rect(center=(CENTER, 30))
        screen.blit(text_surf, text_rect)
        # Draw lines (connections)
        for i in range(OUTER_POINTS):
            # Outer ring
            pygame.draw.line(screen, BLACK, self.positions[i], self.positions[(i+1)%OUTER_POINTS], 2)
            # Spokes
            pygame.draw.line(screen, BLACK, self.positions[i], self.positions[8], 2)
        # Draw points
        for i, (x, y) in enumerate(self.positions):
            pygame.draw.circle(screen, GREY, (x, y), PIECE_RADIUS)
        # Draw pieces
        for i, (x, y) in enumerate(self.positions):
            if self.state[i] == 1:
                pygame.draw.circle(screen, WHITE, (x, y), PIECE_RADIUS-5)
                pygame.draw.circle(screen, BLACK, (x, y), PIECE_RADIUS-5, 2)
            elif self.state[i] == 2:
                pygame.draw.circle(screen, BLACK, (x, y), PIECE_RADIUS-5)
                pygame.draw.circle(screen, BLACK, (x, y), PIECE_RADIUS-5, 2)
            # Highlight selected piece
            if self.selected == i:
                pygame.draw.circle(screen, (0, 255, 0), (x, y), PIECE_RADIUS-10, 3)
        # Draw win message
        if self.win_message:
            win_font = pygame.font.SysFont(None, 48)
            win_surf = win_font.render(self.win_message, True, (200, 0, 0))
            win_rect = win_surf.get_rect(center=(CENTER, 70))
            screen.blit(win_surf, win_rect)

    def get_state(self):
        return self.state

    def get_positions(self):
        return self.positions

    def get_adjacent(self, idx):
        # Returns a list of indices adjacent to idx
        # Outer points: adjacent to next/prev and center
        if idx == 8:
            # Center: adjacent to all outer points
            return list(range(8))
        else:
            return [(idx - 1) % 8, (idx + 1) % 8, 8]

    def player_has_moves(self, player):
        for i in range(9):
            if self.state[i] == player:
                for adj in self.get_adjacent(i):
                    if self.state[adj] == 0:
                        return True
        return False

    def animate_move(self, from_idx, to_idx):
        start_pos = self.positions[from_idx]
        end_pos = self.positions[to_idx]
        color = WHITE if self.state[from_idx] == 1 else BLACK
        steps = 20
        for step in range(1, steps + 1):
            t = step / steps
            x = int(start_pos[0] * (1 - t) + end_pos[0] * t)
            y = int(start_pos[1] * (1 - t) + end_pos[1] * t)
            self.draw(self.screen)
            pygame.draw.circle(self.screen, color, (x, y), PIECE_RADIUS-5)
            pygame.draw.circle(self.screen, BLACK, (x, y), PIECE_RADIUS-5, 2)
            pygame.display.flip()
            pygame.time.delay(10)

    def ai_move(self):
        # Check if game is over
        if self.win_message:
            return

        # move = ai.ai_random_move(self.state, self.current_player)
        # move = ai.ai_minimax_move(self.state, self.current_player)
        if self.ai_mode == "random":
            move = ai.ai_random_move(self.state, self.current_player)
        elif self.ai_mode == "minimax":
            move = ai.ai_minimax_move(self.state, self.current_player)

        if move:
            from_idx, to_idx = move
            # If the piece is moving to the center, check if it's adjacent to an opponent's piece
            if to_idx == 8:
                opponent = 2 if self.current_player == 1 else 1
                adj = self.get_adjacent(from_idx)
                if not any(self.state[a] == opponent for a in adj):
                    winner = "White" if self.current_player == 1 else "Black"
                    print("AI cannot move to the center unless the piece is adjacent to an opponent's piece!")
                    self.win_message = f"{winner} wins!"
                    return
            self.animate_move(from_idx, to_idx)
            self.state[to_idx] = self.state[from_idx]
            self.state[from_idx] = 0
            # Switch player
            self.current_player = 2 if self.current_player == 1 else 1
            # Check if next player can move
            if not self.player_has_moves(self.current_player):
                winner = "White" if self.current_player == 1 else "Black"
                print(f"Player {self.current_player} cannot move. Game over!")
                self.win_message = f"{winner} wins!"
        else:
            print("No move found") # No move found, AI lost
            winner = "White" if self.current_player == 2 else "Black"
            self.win_message = f"{winner} wins!"


    def handle_click(self, pos):

        # Check if game is over
        if self.win_message:
            return

        # Find which point was clicked
        for i, (x, y) in enumerate(self.positions):
            dist = math.hypot(pos[0] - x, pos[1] - y)
            r = CENTER_RADIUS if i == 8 else PIECE_RADIUS
            if dist <= r:
                if self.selected is None:
                    # Select a piece belonging to the current player
                    if self.state[i] == self.current_player:
                        self.selected = i
                else:
                    # Try to move to an empty spot
                    if self.state[i] == 0 and self.selected != i:
                        # Only allow move to adjacent spot
                        if i not in self.get_adjacent(self.selected):
                            print("You can only move to an adjacent spot!")
                            self.selected = None
                            break
                        # Only apply the adjacent-opponent rule if moving to the center
                        if i == 8:
                            opponent = 2 if self.current_player == 1 else 1
                            adj = self.get_adjacent(self.selected)
                            if not any(self.state[a] == opponent for a in adj):
                                print("You can only move to the center if your piece is adjacent to an opponent's piece!")
                                self.selected = None
                                break
                        self.animate_move(self.selected, i)
                        self.state[i] = self.state[self.selected]
                        self.state[self.selected] = 0
                        self.selected = None
                        # Mark first move as done if it was the first move
                        if not self.first_move_done:
                            self.first_move_done = True
                        # Switch player
                        self.current_player = 2 if self.current_player == 1 else 1
                        # Check if next player can move
                        if not self.player_has_moves(self.current_player):
                            print(f"Player {self.current_player} cannot move. Game over!")
                        # If playing vs AI and it's now AI's turn, make AI move
                        if self.num_players == 1 and self.current_player != self.player_color:
                            self.ai_move()
                    elif self.state[i] == self.current_player:
                        # Select a different piece
                        self.selected = i
                break

# For testing: run this file to display the board
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Mutorere Board")
    board = Board(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_click(event.pos)
        board.draw(screen)
        pygame.display.flip()
    pygame.quit()
