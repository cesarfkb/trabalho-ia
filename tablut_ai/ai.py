# Functions to be made
# count_pieces(board, player)
# find_king(board)
# get_possible_moves(board, player)
# get_possible_move_piece(board, index)
# get_best_move(board, player)
# min_distance_to_edge(board, player)
# minimax(board, depth, player, alpha, beta)

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

player_pieces = {1: [], 2: []}  # Store pieces for each player

def update_player_pieces(board):
    global player_pieces
    player_pieces[1] = [i for i in range(len(board)) if board[i] == 1]
    player_pieces[2] = [i for i in range(len(board)) if board[i] == 2 or board[i] == 3]  # Include king for player 2

def count_pieces(board, player):
    return sum(1 for piece in board if piece == player)

def find_king(board): # if board[index] == 3 it's the king
    for i in range(len(board)):
        if board[i] == 3:
            return i
    return None

def get_possible_moves(board, player):
    print(f"Getting possible moves for player {player}")
    possible_moves = []

    for i in range(len(board)):
        if board[i] == player or (player == 2 and board[i] == 3):  # Include king for player 2
            piece_moves = get_possible_move_piece(board, i)
            for move in piece_moves:
                possible_moves.append((i, move))
    return possible_moves

def get_possible_move_piece(board, index):
    print(f"Getting possible moves for piece at index {index}")
    
    possible_moves = []
    row = index // 9
    col = index % 9

    for dr, dc in DIRECTIONS:
        r, c = row, col
        while True:
            r += dr
            c += dc
            if 0 <= r < 9 and 0 <= c < 9:
                new_index = r * 9 + c
                if board[new_index] == 0:
                    possible_moves.append(new_index)
                else: 
                    break
            else:
                break

    return possible_moves

def is_piece_blocked(board, index):
    row = index // 9
    col = index % 9
    
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if 0 <= r < 9 and 0 <= c < 9:
            new_index = r * 9 + c
            if board[new_index] == 0:
                return False
    return True

def count_attackers_king(board, king_index):
    attackers = 0
    row = king_index // 9
    col = king_index % 9
    
    # If King is in the castle, check only adjacent squares
    if (row == 4 and col == 4):
        for dr, dc in DIRECTIONS:
            r = row + dr
            c = col + dc
            if 0 <= r < 9 and 0 <= c < 9:
                new_index = r * 9 + c
                if board[new_index] == 1:
                    attackers += 1
    # Elif king is besides the castle
    if (row == 4 and col == 3) or (row == 4 and col == 5) or (row == 3 and col == 4) or (row == 5 and col == 4):
        for dr, dc in DIRECTIONS:
            r = row + dr
            c = col + dc
            if 0 <= r < 9 and 0 <= c < 9:
                new_index = r * 9 + c
                if board[new_index] == 1:
                    attackers += 1
                elif (r == 4 and c == 4) and board[new_index] == 0:
                    attackers += 1
    
    # If King is not in the castle, and not beside it, normal rules apply
    else:
        for dr, dc in DIRECTIONS:
            r = row + dr
            c = col + dc
            if 0 <= r < 9 and 0 <= c < 9:
                new_index = r * 9 + c
                if board[new_index] == 1:
                    attackers += 1

    return attackers

def evaluate_board(board, player):
    opponent = 1 if player == 2 else 2
    player_pieces = count_pieces(board, player)
    opponent_pieces = count_pieces(board, opponent)
    king_position = find_king(board)
    score = 0


    # Calculate score based on pieces count
    score += player_pieces - opponent_pieces * 2

    # Calculate score based on potential captures
    score += reward_potential_capture(board, player)

    # Calculate distance to edge for the king
    if king_position is not None:
        king_row = king_position // 9
        king_col = king_position % 9
        
        if player == 2:
            score += reward_clear_path_to_edge(board, king_row, king_col, player)
        else:
            score -= reward_clear_path_to_edge(board, king_row, king_col, player)

        # Success reward if king is on the edge
        if king_row == 0 or king_row == 8 or king_col == 0 or king_col == 8:
            if player == 2:
                return float('inf')
            else:
                return float('-inf')

    # Check attackers around the king
    if king_position is not None:
        king_row = king_position // 9
        king_col = king_position % 9
        attackers = count_attackers_king(board, king_position)
        if player == 1:
            score += attackers * 40
        else:
            score -= attackers * 100

    # Penalty if defenders are too far from the king

    return score

def reward_clear_path_to_edge(board, king_row, king_col, player):
    reward = 0

    for dr, dc in DIRECTIONS:
        r, c = king_row, king_col
        steps = 0
        clear_path = True

        while 0 <= r < 9 and 0 <= c < 9:
            r += dr
            c += dc
            if 0 <= r < 9 and 0 <= c < 9:
                index = r * 9 + c
                if board[index] != 0:  # Path is blocked by a piece
                    clear_path = False
                    break
                steps += 1

                # Special reward for reaching the edge
                if r == 0 or r == 8 or c == 0 or c == 8:
                    reward += 1000  # Huge reward for reaching the edge
                    break

        if clear_path:
            reward += steps * 50  # Reward for clear path (adjust weight as needed)

    return reward

def reward_potential_capture(board, player):
    opponent = 1 if player == 2 else 2
    reward = 0
    for i in range(len(board)):
        if board[i] == player or (player == 2 and board[i] == 3):
            row = i // 9
            col = i % 9
            for dr, dc in DIRECTIONS:
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 9:
                    new_index = r * 9 + c
                    if board[new_index] == opponent:
                        # Check if the opponent's piece is adjacent to another opponent's piece
                        for dr2, dc2 in DIRECTIONS:
                            r2, c2 = r + dr2, c + dc2
                            if 0 <= r2 < 9 and 0 <= c2 < 9:
                                new_index2 = r2 * 9 + c2
                                if board[new_index2] == opponent:
                                    reward += 10
    return reward

def simulate_move(board, move):
    print(f"Simulating move: {move}")
    new_board = board[:]
    from_index, to_index = move
    new_board[to_index] = new_board[from_index]
    new_board[from_index] = 0
    return new_board

def minimax(board, depth, player, maximizing_player, alpha, beta):
    if depth == 0 or not get_possible_moves(board, player):
        return evaluate_board(board, player)

    opponent = 1 if player == 2 else 2
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(board, player):
            new_board = simulate_move(board, move)
            eval = minimax(new_board, depth - 1, opponent, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(board, player):
            new_board = simulate_move(board, move)
            eval = minimax(new_board, depth - 1, opponent, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, player, depth=3):
    print(f"Calculating best move for player {player} with depth {depth}")
    best_move = None
    best_value = float('-inf') if player == 2 else float('inf')
    opponent = 1 if player == 2 else 2

    # Check for moves that give the king a clear path to the edge
    for move in get_possible_moves(board, player):
        from_index, to_index = move
        if board[from_index] == 3:  # If the piece being moved is the king
            king_row = to_index // 9
            king_col = to_index % 9
            if reward_clear_path_to_edge(board, king_row, king_col, player) > 0:
                print(f"King has a clear path to the edge with move: {move}")
                return move  # Return the move immediately

    # If no instant winning move is found, proceed with Minimax
    for move in get_possible_moves(board, player):
        print(f"Evaluating move: {move}")
        new_board = simulate_move(board, move)
        move_value = minimax(new_board, depth - 1, opponent, not(player == 2), float('-inf'), float('inf'))
        
        if (player == 2 and move_value > best_value) or (player == 1 and move_value < best_value):
            best_value = move_value
            best_move = move

    return best_move