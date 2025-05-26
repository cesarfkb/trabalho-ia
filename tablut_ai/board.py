import pygame
import sys
import ai

# Board Constants
WINDOW_SIZE = 700  # Total window size
BOARD_SIZE = 600  # Size of the grid area
GRID_SIZE = 9
CELL_SIZE = BOARD_SIZE // GRID_SIZE
BORDER_SIZE = (WINDOW_SIZE - BOARD_SIZE) // 2  # Border around the grid
BORDER_WIDTH = 2
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Tablut")
screen.fill(BACKGROUND_COLOR)

# Global variables
board = [0] * (GRID_SIZE * GRID_SIZE)  # Initialize the board with empty cells
selected_piece = None  # Index of the currently selected piece
current_player = 1  # 1 for black, 2 for white
possible_moves = []  # List of possible moves for the selected piece
king_captured = False  # Flag to check if the king is captured
ai_mode = True  # Flag to check if AI mode is enabled
player_color = 1  # 1 for black, 2 for white


def draw_borders():
    """Draw the borders around the grid."""
    # Draw a slightly thicker border
    pygame.draw.rect(
        screen,
        BORDER_COLOR,
        (BORDER_SIZE, BORDER_SIZE, BOARD_SIZE, BOARD_SIZE),
        BORDER_WIDTH,
    )


def draw_grid():
    """Draw the 9x9 grid inside the bordered area."""
    # Draw interior grid lines only (not outer border)
    for i in range(1, GRID_SIZE):
        # Vertical lines
        x = BORDER_SIZE + i * CELL_SIZE
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (x, BORDER_SIZE + 1),
            (x, BORDER_SIZE + BOARD_SIZE - 1),
            1,
        )
        # Horizontal lines
        y = BORDER_SIZE + i * CELL_SIZE
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (BORDER_SIZE + 1, y),
            (BORDER_SIZE + BOARD_SIZE - 1, y),
            1,
        )

    # Draw an X in the center cell (4, 4)
    center_x = BORDER_SIZE + 4 * CELL_SIZE
    center_y = BORDER_SIZE + 4 * CELL_SIZE
    pygame.draw.line(
        screen,
        LINE_COLOR,
        (center_x, center_y),
        (center_x + CELL_SIZE, center_y + CELL_SIZE),
        1,
    )
    pygame.draw.line(
        screen,
        LINE_COLOR,
        (center_x + CELL_SIZE, center_y),
        (center_x, center_y + CELL_SIZE),
        1,
    )
    # Draw a small circle outline in the center of the corner cells (0, 0), (0, 8), (8, 0), (8, 8)
    # Corner (0, 0)
    pygame.draw.circle(
        screen,
        LINE_COLOR,
        (BORDER_SIZE + CELL_SIZE // 2, BORDER_SIZE + CELL_SIZE // 2),
        CELL_SIZE // 6,
        1,
    )
    # Corner (0, 8)
    pygame.draw.circle(
        screen,
        LINE_COLOR,
        (BORDER_SIZE + CELL_SIZE // 2, BORDER_SIZE + BOARD_SIZE - CELL_SIZE // 2),
        CELL_SIZE // 6,
        1,
    )
    # Corner (8, 0)
    pygame.draw.circle(
        screen,
        LINE_COLOR,
        (BORDER_SIZE + BOARD_SIZE - CELL_SIZE // 2, BORDER_SIZE + CELL_SIZE // 2),
        CELL_SIZE // 6,
        1,
    )
    # Corner (8, 8)
    pygame.draw.circle(
        screen,
        LINE_COLOR,
        (
            BORDER_SIZE + BOARD_SIZE - CELL_SIZE // 2,
            BORDER_SIZE + BOARD_SIZE - CELL_SIZE // 2,
        ),
        CELL_SIZE // 6,
        1,
    )


def draw_pieces(board):
    for i in range(len(board)):
        if board[i] == 0:
            continue
        row = i // GRID_SIZE
        col = i % GRID_SIZE

        # Find the center of the cell
        center_x = BORDER_SIZE + col * CELL_SIZE + CELL_SIZE // 2
        center_y = BORDER_SIZE + row * CELL_SIZE + CELL_SIZE // 2

        # Draw the pieces
        if board[i] == 3:  # Draw king
            color = (255, 255, 255)
            pygame.draw.circle(screen, color, (center_x, center_y), CELL_SIZE // 2.5)
            # Draw a square inside the circle
            pygame.draw.rect(
                screen,
                LINE_COLOR,
                (
                    center_x - CELL_SIZE // 5,
                    center_y - CELL_SIZE // 5,
                    CELL_SIZE // 2.5,
                    CELL_SIZE // 2.5,
                ),
                1,
            )
            pygame.draw.circle(
                screen, LINE_COLOR, (center_x, center_y), CELL_SIZE // 2.5, 1
            )
        else:  # Draw normal pieces
            color = (0, 0, 0) if board[i] == 1 else (255, 255, 255)
            pygame.draw.circle(screen, color, (center_x, center_y), CELL_SIZE // 3)
            pygame.draw.circle(
                screen, LINE_COLOR, (center_x, center_y), CELL_SIZE // 3, 1
            )


def draw_selected_piece():
    # Draw a green circle around the selected piece
    if selected_piece is not None:
        row = selected_piece // GRID_SIZE
        col = selected_piece % GRID_SIZE
        center_x = BORDER_SIZE + col * CELL_SIZE + CELL_SIZE // 2
        center_y = BORDER_SIZE + row * CELL_SIZE + CELL_SIZE // 2
        # Draw a bigger circle if its the king
        if board[selected_piece] == 3:
            pygame.draw.circle(
                screen, (0, 255, 0), (center_x, center_y), CELL_SIZE // 2.5, 3
            )
        else:
            pygame.draw.circle(
                screen, (0, 255, 0), (center_x, center_y), CELL_SIZE // 3, 3
            )


def get_possible_moves(piece):
    """Get possible moves for the selected piece."""
    possible_moves = []

    if piece is None:
        return possible_moves

    # RULE - If the center is empty, no one can move to it or jump over it

    # Horizontal moves to the left
    for i in range(1, GRID_SIZE):
        left_index = piece - i
        if left_index < 0 or (piece // GRID_SIZE) != (left_index // GRID_SIZE):
            break
        if board[left_index] == 0:
            if left_index == 40:
                break
            possible_moves.append(left_index)
        else:
            break
    # Horizontal moves to the right
    for i in range(1, GRID_SIZE):
        right_index = piece + i
        if right_index >= len(board) or (piece // GRID_SIZE) != (
            right_index // GRID_SIZE
        ):
            break
        if board[right_index] == 0:
            if right_index == 40:
                break
            possible_moves.append(right_index)
        else:
            break
    # Vertical moves up
    for i in range(1, GRID_SIZE):
        up_index = piece - i * GRID_SIZE
        if up_index < 0:
            break
        if board[up_index] == 0:
            if up_index == 40:
                break
            possible_moves.append(up_index)
        else:
            break
    # Vertical moves down
    for i in range(1, GRID_SIZE):
        down_index = piece + i * GRID_SIZE
        if down_index >= len(board):
            break
        if board[down_index] == 0:
            if down_index == 40:
                break
            possible_moves.append(down_index)
        else:
            break
    return possible_moves


def draw_possible_moves():

    if selected_piece is None:
        return

    # Draw a small gray circle around the possible moves
    for move in possible_moves:
        row = move // GRID_SIZE
        col = move % GRID_SIZE
        center_x = BORDER_SIZE + col * CELL_SIZE + CELL_SIZE // 2
        center_y = BORDER_SIZE + row * CELL_SIZE + CELL_SIZE // 2
        # Draw a small gray circle around the possible moves
        pygame.draw.circle(
            screen, (200, 200, 200), (center_x, center_y), CELL_SIZE // 6
        )


def draw():
    """Draw the entire board."""
    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    draw_borders()
    draw_grid()
    draw_pieces(board)
    draw_selected_piece()
    draw_possible_moves()


def horizontal_adjacent(index):
    # Returns the values of the pieces to the left and right of the index
    left_index = index - 1 if index % GRID_SIZE != 0 else None
    right_index = index + 1 if index % GRID_SIZE != GRID_SIZE - 1 else None
    return (
        board[left_index] if left_index is not None else None,
        board[right_index] if right_index is not None else None,
    )


def vertical_adjacent(index):
    # Returns the values of the pieces above and below the index
    up_index = index - GRID_SIZE if index - GRID_SIZE >= 0 else None
    down_index = index + GRID_SIZE if index + GRID_SIZE < len(board) else None
    return (
        board[up_index] if up_index is not None else None,
        board[down_index] if down_index is not None else None,
    )


def check_capture(index):
    print(f"Checking capture for index {index}")
    global board
    current_player = board[index]
    opponent_player = 2 if current_player == 1 else 1
    king_position = None  # Position of the king, if it is near the checked piece
    global king_captured

    # Check individual adjacent pieces
    left_piece, right_piece = horizontal_adjacent(index)
    up_piece, down_piece = vertical_adjacent(index)

    # Check if we're capturing the king
    if current_player == 1:  # Only black can capture the king
        if up_piece == 3:
            king_position = index - GRID_SIZE
        elif down_piece == 3:
            king_position = index + GRID_SIZE
        elif left_piece == 3:
            king_position = index - 1
        elif right_piece == 3:
            king_position = index + 1
        if king_position is not None:
            # Check if the king is captured
            king_captured = check_king_capture(king_position)

    # Check upwards capture
    if up_piece is not None and index - 2 * GRID_SIZE >= 0:
        up_up_piece = board[index - 2 * GRID_SIZE]
        if up_piece == opponent_player:
            # Check if the piece above the opponent piece is another player's piece
            if up_up_piece == current_player:
                # Capture the opponent piece
                board[index - GRID_SIZE] = 0
                print(f"Captured piece at index {index - GRID_SIZE}")
            if up_up_piece == 3 and current_player == 2:
                # Capture the opponent piece
                board[index - GRID_SIZE] = 0
                print(f"Captured piece at index {index - GRID_SIZE}")
            # If up_up_piece is empty, but is middle of the board
            if up_up_piece == 0 and index - GRID_SIZE == 40:
                # Capture the opponent piece
                board[index - GRID_SIZE] = 0
                print(f"Captured piece at index {index - GRID_SIZE}")

    # Check downwards capture
    if down_piece is not None and index + 2 * GRID_SIZE < len(board):
        down_down_piece = board[index + 2 * GRID_SIZE]
        if down_piece == opponent_player:
            # Check if the piece below the opponent piece is another player's piece
            if down_down_piece == current_player:
                # Capture the opponent piece
                board[index + GRID_SIZE] = 0
                print(f"Captured piece at index {index + GRID_SIZE}")
            if down_down_piece == 3 and current_player == 1:
                # Capture the opponent piece
                board[index + GRID_SIZE] = 0
                print(f"Captured piece at index {index + GRID_SIZE}")
            # If down_down_piece is empty, but is middle of the board
            if down_down_piece == 0 and index + GRID_SIZE == 40:
                # Capture the opponent piece
                board[index + GRID_SIZE] = 0
                print(f"Captured piece at index {index + GRID_SIZE}")

    # Check leftwards capture
    if left_piece is not None and index - 2 >= 0:
        left_left_piece = board[index - 2]
        if left_piece == opponent_player:
            # Check if the piece to the left of the opponent piece is another player's piece
            if left_left_piece == current_player:
                # Capture the opponent piece
                board[index - 1] = 0
                print(f"Captured piece at index {index - 1}")
            if left_left_piece == 3 and current_player == 1:
                # Capture the opponent piece
                board[index - 1] = 0
                print(f"Captured piece at index {index - 1}")
            # If left_left_piece is empty, but is middle of the board
            if left_left_piece == 0 and index - 1 == 40:
                # Capture the opponent piece
                board[index - 1] = 0
                print(f"Captured piece at index {index - 1}")

    # Check rightwards capture
    if right_piece is not None and index + 2 < len(board):
        right_right_piece = board[index + 2]
        if right_piece == opponent_player:
            # Check if the piece to the right of the opponent piece is another player's piece
            if right_right_piece == current_player:
                # Capture the opponent piece
                board[index + 1] = 0
                print(f"Captured piece at index {index + 1}")
            if right_right_piece == 3 and current_player == 2:
                # Capture the opponent piece
                board[index + 1] = 0
                print(f"Captured piece at index {index + 1}")
            # If right_right_piece is empty, but is middle of the board
            if right_right_piece == 0 and index + 1 == 40:
                # Capture the opponent piece
                board[index + 1] = 0
                print(f"Captured piece at index {index + 1}")


def check_king_capture(index):
    # Index is the index of the king
    global board

    left_piece, right_piece = horizontal_adjacent(index)
    up_piece, down_piece = vertical_adjacent(index)

    # Check if the king is in the center of the board
    if index == 40:
        # Check if the king is surrounded by opponent pieces on all sides
        if left_piece == 1 and right_piece == 1 and up_piece == 1 and down_piece == 1:
            # Capture the king
            # board[index] = 0
            print(f"Captured king at index {index}")
            return True
    # Check if the king is adjacent to the center of the board (up, down, left, right)
    elif index == 39:
        # Check if the king is surrounded by opponent pieces on all sides beside the center
        if left_piece == 1 and up_piece == 1 and down_piece == 1:
            # Capture the king
            # board[index] = 0
            print(f"Captured king at index {index}")
            return True
    elif index == 41:
        # Check if the king is surrounded by opponent pieces on all sides beside the center
        if right_piece == 1 and up_piece == 1 and down_piece == 1:
            # Capture the king
            # board[index] = 0
            print(f"Captured king at index {index}")
            return True
    elif index == 31:
        # Check if the king is surrounded by opponent pieces on all sides beside the center
        if left_piece == 1 and up_piece == 1 and right_piece == 1:
            # Capture the king
            # board[index] = 0
            print(f"Captured king at index {index}")
            return True
    elif index == 49:
        # Check if the king is surrounded by opponent pieces on all sides beside the center
        if right_piece == 1 and up_piece == 1 and left_piece == 1:
            # Capture the king
            # board[index] = 0
            print(f"Captured king at index {index}")
            return True
    else:  # Capture as normal piece
        if (left_piece == 1 and right_piece == 1) or (
            up_piece == 1 and down_piece == 1
        ):
            # Capture the king
            # board[index] = 0
            print(f"Captured king at index {index}")
            return True
    return False


def ai_move():
    print("AI is making a move...")
    global current_player
    move = ai.get_best_move(board, current_player, 3)
    print(f"AI move: {move}")
    if move is not None:
        from_index, to_index = move
        board[to_index] = board[from_index]
        board[from_index] = 0
        # After moving, check if there's a capture
        check_capture(to_index)
        # After moving, check if the piece is a king
        if board[to_index] == 3:
            # Check if the king is on the edge of the board
            if (
                to_index % GRID_SIZE == 0
                or to_index % GRID_SIZE == GRID_SIZE - 1
                or to_index // GRID_SIZE == 0
                or to_index // GRID_SIZE == GRID_SIZE - 1
            ):
                # If it is, the game is over
                print("Winner: White")
                current_player = 0


def handle_click(pos):
    """Handle mouse click events."""
    x, y = pos
    # Check if the click is within the grid area
    if (BORDER_SIZE < x < BORDER_SIZE + BOARD_SIZE) and (
        BORDER_SIZE < y < BORDER_SIZE + BOARD_SIZE
    ):
        # Calculate the row and column of the clicked cell
        col = (x - BORDER_SIZE) // CELL_SIZE
        row = (y - BORDER_SIZE) // CELL_SIZE
        index = row * GRID_SIZE + col

        global selected_piece
        global current_player

        if ai_mode and current_player != player_color:
            ai_move()
            current_player = player_color
            return

        # Check if the clicked cell is a piece
        if board[index] != 0:
            if board[index] == 3:
                # If the clicked piece is the king, select it
                selected_piece = index if current_player == 2 else selected_piece
            else:
                selected_piece = index if current_player == board[index] else None

            global possible_moves
            possible_moves = get_possible_moves(selected_piece)
        else:  # If the clicked cell is empty and in possible moves
            if selected_piece is not None and index in possible_moves:
                # Move the piece to the clicked cell
                board[index] = board[selected_piece]
                board[selected_piece] = 0
                selected_piece = None
                possible_moves = []
                # After moving, check if there's a capture
                check_capture(index)
                # After moving, check if the piece is a king
                # If king, check if it is on the edges of the board
                if board[index] == 3:
                    # Check if the king is on the edge of the board
                    if (
                        index % GRID_SIZE == 0
                        or index % GRID_SIZE == GRID_SIZE - 1
                        or index // GRID_SIZE == 0
                        or index // GRID_SIZE == GRID_SIZE - 1
                    ):
                        # If it is, the game is over
                        print("Winner: White")
                        current_player = 0  # Lock the game
                # Check if the king is captured
                elif king_captured:
                    print("Winner: Black")
                    current_player = 0
                    # Lock the game
                else:
                    # Switch player
                    current_player = 2 if current_player == 1 else 1


def draw_numbers():  # Debug to check the grid and pieces numbers
    # Draw numbers on the grid
    font = pygame.font.Font(None, 36)
    for i in range(GRID_SIZE):
        # Draw row numbers
        text = font.render(str(i + 1), True, LINE_COLOR)
        screen.blit(
            text,
            (
                BORDER_SIZE - 30,
                BORDER_SIZE + i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2,
            ),
        )
        # Draw column numbers
        text = font.render(str(i + 1), True, LINE_COLOR)
        screen.blit(
            text,
            (
                BORDER_SIZE + i * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2,
                BORDER_SIZE + BOARD_SIZE,
            ),
        )
        # Draw from 0 to 80 in each cell individually
        for j in range(GRID_SIZE):
            text = font.render(str(i * GRID_SIZE + j), True, LINE_COLOR)
            screen.blit(
                text,
                (
                    BORDER_SIZE
                    + j * CELL_SIZE
                    + CELL_SIZE // 2
                    - text.get_width() // 2,
                    BORDER_SIZE
                    + i * CELL_SIZE
                    + CELL_SIZE // 2
                    - text.get_height() // 2,
                ),
            )


def main():
    """Main game loop."""
    # Board state: 0=empty, 1=black, 2=white, 3=king
    global board
    board = [
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        1,
        1,
        1,
        2,
        2,
        3,
        2,
        2,
        1,
        1,
        1,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
    ]
    draw()  # draw and update the board
    # draw_numbers()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)
        draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
