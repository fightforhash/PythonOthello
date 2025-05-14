#from backend import get_legal_moves, make_move, is_game_over, eval_board

import copy
from constants import CELL_SIZE, BOARD_COLOR, HIGHLIGHT_COLOR, WHITE_COLOR, BLACK_COLOR,POSSIBLE_MOVE_COLOR, EMPTY, BLACK, WHITE


# Othello AI class
class OthelloAI:
    def __init__(self, difficulty):
        self.max_depth = {'easy': 2, 'medium': 4, 'hard': 6, 'expert': 8}.get(difficulty, 4)

    def make_move(self, board, player):
        _, move = self.alpha_beta_search(board, player, self.max_depth)
        return move

    def alpha_beta_search(self, board, player, max_depth, alpha=-float('inf'), beta=float('inf')):
        from backend import eval_board, get_legal_moves, make_move, is_game_over
        if max_depth == 0 or is_game_over(board):
            return eval_board(board, player), None

        if player == BLACK:
            max_eval, best_move = -float('inf'), None
            for move in get_legal_moves(board, player):
                new_board = make_move(copy.deepcopy(board), move, player)
                eval = self.alpha_beta_search(new_board, WHITE, max_depth - 1, alpha, beta)[0]
                if eval > max_eval:
                    max_eval, best_move = eval, move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval, best_move = float('inf'), None
            for move in get_legal_moves(board, player):
                new_board = make_move(copy.deepcopy(board), move, player)
                eval = self.alpha_beta_search(new_board, BLACK, max_depth - 1, alpha, beta)[0]
                if eval < min_eval:
                    min_eval, best_move = eval, move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
        