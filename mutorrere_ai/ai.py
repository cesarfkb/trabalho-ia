# AI for the Mutorere game

# 1st AI - Random moves

import random

def ai_random_move(state, current_player):
    # state: list of 9 ints (0=empty, 1=white, 2=black)
    # current_player: 1 or 2
    # Returns (from_idx, to_idx) for a valid move
    # Board adjacency (same as Board.get_adjacent)
    def get_adjacent(idx):
        if idx == 8:
            return list(range(8))
        else:
            return [(idx - 1) % 8, (idx + 1) % 8, 8]
    opponent = 2 if current_player == 1 else 1
    moves = []
    # Special case: AI is white and it's the first move
    if current_player == 1 and state.count(1) == 4: 
        # Find all white pieces adjacent to a black piece
        for i in range(9):
            if state[i] == 1:
                if any(state[a] == 2 for a in get_adjacent(i)):
                    # Find an empty adjacent spot
                    for adj in get_adjacent(i):
                        if state[adj] == 0:
                            # Always pick the first valid move found
                            return (i, adj)
    
    # Get all valid moves
    for i in range(9):
        if state[i] == current_player:
            for adj in get_adjacent(i):
                if state[adj] == 0:
                    # Check if the move is to the center
                    if adj == 8:
                        # Check if the piece is adjacent to an opponent's piece
                        if not any(state[a] == opponent for a in get_adjacent(i)):
                            continue
                    moves.append((i, adj))
    if moves:
        return random.choice(moves)
    else:
        return None

# 2nd AI - Minimax
def ai_minimax_move(state, current_player, depth=5):
    def get_adjacent(idx):
        if idx == 8:
            return list(range(8))
        else:
            return [(idx - 1) % 8, (idx + 1) % 8, 8]

    def valid_moves(state, player):
        opponent = 2 if player == 1 else 1
        moves = []
        for i in range(9):
            if state[i] == player:
                for adj in get_adjacent(i):
                    if state[adj] == 0:
                        # Check if the move is to the center
                        if adj == 8:
                            # Check if the piece is adjacent to an opponent's piece
                            if not any(state[a] == opponent for a in get_adjacent(i)):
                                continue
                        moves.append((i, adj))
        return moves

    def evaluate(state, player):
        # Simple evaluation: number of moves for player minus for opponent
        ai_moves = len(valid_moves(state, player))
        player_moves = len(valid_moves(state, 2 if player == 1 else 1))
        # If ai has no moves, they lose
        if ai_moves == 0:
            return float('-inf')
        # If player has no moves, ai wins
        if player_moves == 0:
            return float('inf')
        return ai_moves - player_moves

    def minimax(state, player, depth, maximizing):
        moves = valid_moves(state, player)
        if depth == 0 or not moves:
            return evaluate(state, current_player), None
        if maximizing:
            best_score = float('-inf')
            best_move = None
            for move in moves:
                new_state = state[:]
                new_state[move[1]] = new_state[move[0]]
                new_state[move[0]] = 0
                
                # Doing Minimax for the opponent (minimizing)
                score, _ = minimax(new_state, 2 if player == 1 else 1, depth-1, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in moves:
                new_state = state[:]
                new_state[move[1]] = new_state[move[0]]
                new_state[move[0]] = 0
                score, _ = minimax(new_state, 2 if player == 1 else 1, depth-1, True)
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    _, best_move = minimax(state, current_player, depth, True)
    return best_move