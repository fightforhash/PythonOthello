from constants import EMPTY, BLACK, WHITE
import AI

# OthelloBoard
class OthelloBoard:
    def __init__(self):
        self.board = self.new_board()

    def new_board(self):
        board = [[EMPTY for _ in range(8)] for _ in range(8)]
        board[3][3], board[3][4] = WHITE, BLACK
        board[4][3], board[4][4] = BLACK, WHITE
        return board
#constantly prints out the board state
    def print_board(self, current_player):
        print("--- Current Board ---")
        legal_moves = get_legal_moves(self.board, current_player)
        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if cell == EMPTY and (r, c) in legal_moves:
                    print('O', end=' ')
                else:
                    print('1' if cell == WHITE else '0' if cell == BLACK else '.', end=' ')
            print()
        print("--------------------")

# Helper functions for AI and game logic
def get_legal_moves(board, player):
    legal_moves = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == EMPTY and any(
                matches := check_direction(board, row, col, d_row, d_col, player)
                for d_row, d_col in directions()
            ):
                legal_moves.append((row, col))
    return legal_moves

def make_move(board, move, player):
    row, col = move
    if board[row][col] != EMPTY:
        return board  # Invalid move

    board[row][col] = player  # Place the piece on the board
    for d_row, d_col in directions():
        if matches := check_direction(board, row, col, d_row, d_col, player):
            for m_row, m_col in matches:
                board[m_row][m_col] = player  # Flip the opponent's pieces
    return board

def is_game_over(board):
    return not any(get_legal_moves(board, BLACK)) and not any(get_legal_moves(board, WHITE))

def eval_board(board, player):
    return sum(row.count(player) - row.count(opponent(player)) for row in board)

def opponent(player):
    return BLACK if player == WHITE else WHITE

def check_direction(board, row, col, d_row, d_col, player):
    opp = opponent(player)
    matches = []
    row, col = row + d_row, col + d_col
    while 0 <= row < 8 and 0 <= col < 8 and board[row][col] == opp:
        matches.append((row, col))
        row, col = row + d_row, col + d_col
    if 0 <= row < 8 and 0 <= col < 8 and board[row][col] == player:
        return matches
    return []

def directions():
    return [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]

# Game logic functions 
def is_legal_move(board, player, row, col):
    return board[row][col] == EMPTY and any(
        matches := check_direction(board, row, col, d_row, d_col, player)
        for d_row, d_col in directions()
    )

def play_game(play_with_ai, ai_difficulty='medium'):
    board = OthelloBoard()
    ai = AI.OthelloAI(ai_difficulty) if play_with_ai else None
    current_player = BLACK
    game_over = False

    while not game_over:
        board.print_board(current_player)
        if not get_legal_moves(board.board, current_player):
            print(f"No valid moves for {'Black' if current_player == BLACK else 'White'}. Turn skipped.")
            current_player = opponent(current_player)
            continue

        move = None
        if current_player == BLACK or not play_with_ai:
            move = get_player_move(board.board, current_player)
            if move is None:  # Check if the player chose to quit
                print("Player has exited the game.")
                return  # Exit the play_game function
        else:
            move = ai.make_move(board.board, current_player)

        if move:
            board.board = make_move(board.board, move, current_player)
        else:
            print("No move made, game will exit.")
            return

        current_player = opponent(current_player)
        game_over = is_game_over(board.board)

    final_score = eval_board(board.board, BLACK)
    print("Game over! Final board:")
    board.print_board()
    if final_score > 0:
        print(f"Black wins by {final_score}!")
    elif final_score < 0:
        print(f"White wins by {-final_score}!")
    else:
        print("It's a tie!")

def get_player_move(board, player):
    while True:  # Keep asking for input until a legal move or 'quit' is entered
        move_input = input(f"Player {'Black' if player == BLACK else 'White'}, enter your move (row col), or type 'quit' to exit: ")
        if move_input.lower() == 'quit':  # Check if the user wants to quit
            print("Exiting the game.")
            return None  # None indicates the player chose to quit

        try:
            row, col = map(int, move_input.split())
            if is_legal_move(board, player, row, col):
                return row, col
            else:
                print("That is not a legal move. Please try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column numbers separated by a space.")


