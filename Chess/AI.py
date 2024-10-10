import copy
import math
import random
from constaints import *

class AI:
    def __init__(self, depth, color):
        self.depth = depth
        self.color = color
        self.moves = []
        self.explored_nodes = 0
    
    def get_moves(self, game_Board, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = game_Board.board[row][col]
                if square.has_Team(color):
                    game_Board.calc_moves(square.piece, row, col)
                    moves += square.piece.moves       
        return moves

    def minimax(self, game_Board, depth, turn, alpha, beta):
        if depth == 0:
            print("Yes")
            return game_Board.evaluate(), None
        
        # White
        if turn == "White":
            max_score = -math.inf
            moves = self.get_moves(game_Board, 'White')
            print(len(moves))
            for move in moves:
                self.explored += 1
                print(self.explored)
                temp_board = copy.deepcopy(game_Board)
                piece = temp_board.board[move[0].row_idx][move[0].col_idx].piece
                temp_board.move_Piece(piece, move)
                piece.is_Moved = False
                score = self.minimax(temp_board, depth-1, "Black", alpha, beta)[0]
                if score > max_score:
                    max_score = score
                    best_move = move

                alpha = max(alpha, max_score)
                if beta <= alpha: break

            if not best_move:
                idx = random.randrange(0, len(moves))
                best_move = moves[idx]

            return max_score, best_move
        
        # Black
        elif turn == "Black":
            min_score = math.inf
            moves = self.get_moves(game_Board, 'Black')
            print(len(moves))
            for move in moves:
                self.explored += 1
                print(self.explored)
                temp_board = copy.deepcopy(game_Board)
                piece = temp_board.board[move[0].row_idx][move[0].col_idx].piece
                temp_board.move_Piece(piece, move)
                piece.is_Moved = False
                score = self.minimax(temp_board, depth-1, "White", alpha, beta)[0]
                if score < min_score:
                    min_score = score
                    best_move = move

                beta = min(beta, min_score)
                if beta <= alpha: break
            
            if not best_move:
                idx = random.randrange(0, len(moves))
                best_move = moves[idx]

            return min_score, best_move
    
    def eval(self, board):
        self.explored = 0

        last_move = board.last_Move
        self.moves.append(last_move)

        print('\nFinding best move...')
                        
        score, move = self.minimax(board, self.depth, "Black", -math.inf, math.inf)
            
        print('\n- Initial eval:', board.evaluate())
        print('- Final eval:', score)
        print('- Boards explored', self.explored)
        if score >= 5000: print('* White MATE!')
        if score <= -5000: print('* Black MATE!')
            
        self.moves.append(move)

        return move