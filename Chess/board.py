import copy
from constaints import *
from piece import *

class Square:
    def __init__(self, row_idx : int, col_idx : int, piece=None):
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.piece = piece
    def has_Piece(self):
        return self.piece != None
    def has_Team(self, color):
        return self.has_Piece() and self.piece.color == color
    def has_Enemy(self, color):
        return self.has_Piece() and self.piece.color != color
    def is_empty_or_has_enemy(self, color):
        return not self.has_Piece() or self.has_Enemy(color)
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
class Board:
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0] for row in range(ROWS)]
        self.last_Move = ()
        self.create_Board()
        self.add_Piece('White')
        self.add_Piece('Black')

    def move_Piece(self, piece, move):
        final_move_col_idx, final_move_row_idx= move[1].col_idx, move[1].row_idx
        inital_move_col_idx, initial_move_row_idx = move[0].col_idx, move[0].row_idx       
        self.board[initial_move_row_idx][inital_move_col_idx].piece = None  
        self.board[final_move_row_idx][final_move_col_idx].piece = piece 
        piece.is_Moved = True
        piece.moves = []
        self.last_Move = move
        if isinstance(piece, Pawn):
            if (piece.color == 'White' and final_move_row_idx == 0) or (piece.color == 'Black' and final_move_row_idx == 7):
                self.board[final_move_row_idx][final_move_col_idx].piece = Queen(piece.color)
    
        if isinstance(piece, King):
            if inital_move_col_idx + 2 == final_move_col_idx:
                initial_rook_Move = Square(initial_move_row_idx, inital_move_col_idx + 3)
                final_rook_Move = Square(initial_move_row_idx, inital_move_col_idx + 1)
                rook_Move = (initial_rook_Move, final_rook_Move)
                self.move_Piece(self.board[final_move_row_idx][final_move_col_idx + 1].piece, rook_Move)
                self.board[initial_move_row_idx][inital_move_col_idx].piece = None  
                self.board[final_move_row_idx][final_move_col_idx].piece = piece 
                self.board[final_move_row_idx][final_move_col_idx].piece.is_Moved = True
                self.board[final_move_row_idx][final_move_col_idx].piece.moves = []
            if inital_move_col_idx - 2 == final_move_col_idx:
                initial_rook_Move = Square(initial_move_row_idx, inital_move_col_idx - 4)
                final_rook_Move = Square(initial_move_row_idx, inital_move_col_idx - 1)
                rook_Move = (initial_rook_Move, final_rook_Move)
                self.move_Piece(self.board[final_move_row_idx][final_move_col_idx - 2].piece, rook_Move)
                self.board[initial_move_row_idx][inital_move_col_idx].piece = None  
                self.board[final_move_row_idx][final_move_col_idx].piece = piece 
                self.board[final_move_row_idx][final_move_col_idx].piece.is_Moved = True
                self.board[final_move_row_idx][final_move_col_idx].piece.moves = []

    def evaluate(self):
        value = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col].piece != None:
                    if self.board[row][col].piece.color == "White":
                        value += piece_square_tables[self.board[row][col].piece.name][row][col]
                    else:
                        value -= piece_square_tables[self.board[row][col].piece.name][7 - row][col]
                    value += self.board[row][col].piece.value
                    if self.board[row][col].piece.name != 'queen': value += 0.01 * len(self.board[row][col].piece.moves)
                    else: value += 0.003 * len(self.board[row][col].piece.moves)
                    value += self.get_threatened_pieces(self.board[row][col].piece, row, col)
        value = round(value, 5)          
        return value

    def check_Checkmate(self, piece, move):
        tmp_Piece = copy.deepcopy(piece)
        tmp_Board = copy.deepcopy(self)
        tmp_Board.move_Piece(tmp_Piece, move)
        for row in range(ROWS):
            for col in range(COLS):
                if tmp_Board.board[row][col].has_Enemy(piece.color):
                    p = tmp_Board.board[row][col].piece
                    tmp_Board.calc_moves(p, row, col, False)
                    for m in p.moves:
                        if isinstance(m[1].piece, King):
                            return True
        return False
    def check_Checkmate_Now(self, turn):
        tmp_Board = copy.deepcopy(self)
        for row in range(ROWS):
            for col in range(COLS):
                if tmp_Board.board[row][col].has_Enemy(turn):
                    p = tmp_Board.board[row][col].piece
                    tmp_Board.calc_moves(p, row, col, False)
                    for m in p.moves:
                        if isinstance(m[1].piece, King):
                            return True
        return False
    
    def get_threatened_pieces(self, piece, row, col):
        # tmp_Board = copy.deepcopy(self)
        # tmp_Board.calc_moves(piece, row, col, False)
        value = 0
        for move in piece.moves:
            if move[1].has_Enemy(piece.color):
                value += move[1].piece.value
        return value

    def has_valid_move(self, turn):
        tmp_Board = copy.deepcopy(self)
        valid_move = []
        for row in range(ROWS):
            for col in range(COLS):
                if tmp_Board.board[row][col].has_Piece() and tmp_Board.board[row][col].piece.color == turn:
                    p = tmp_Board.board[row][col].piece
                    tmp_Board.calc_moves(p, row, col)
                    valid_move.extend(p.moves)
        if len(valid_move) > 0:
            return True
        else:
            return False

    def check_Clear_Path(self, row, col_start, col_end):
        step = 1 if col_end > col_start else -1
        for col in range(col_start + step, col_end, step):
            if self.board[row][col].piece is not None:
                return False
        return True  

    def calc_moves(self, piece, row : int, col : int, bool = True):
        piece.moves = []
        def can_castling(king, rook, row, king_col, rook_col):
            if isinstance(king, King) and isinstance(rook, Rook):
                if king.is_Moved == False and rook.is_Moved == False:
                    if self.check_Clear_Path(row, min(king_col, rook_col), max(king_col, rook_col)):
                        return True
            return False
        def can_Castling_side_King():
            king = self.board[row][4].piece
            rook_side_King = self.board[row][7].piece
            return can_castling(king, rook_side_King, row, 4, 7)
        def can_Castling_side_Queen():
            king = self.board[row][4].piece
            rook_side_Queen = self.board[row][0].piece
            return can_castling(king, rook_side_Queen, row, 4, 0)
        
        def Pawn_move():
            possible_moves = []
            direction = 1 if piece.color == 'Black' else -1
            if row + direction < 8 and row + direction >= 0 and not self.board[row + direction][col].has_Piece():
                possible_moves.append((row + direction, col))
            if (piece.color == 'White' and row == 6) or (piece.color == 'Black' and row == 1):
                if row + 2 * direction < 8 and row + 2 * direction >= 0 and not self.board[row + 2 * direction][col].has_Piece() and not self.board[row + direction][col].has_Piece():
                    possible_moves.append((row + 2 * direction, col))
            if col - 1 >= 0 and self.board[row + direction][col - 1].has_Enemy(piece.color):
                possible_moves.append((row + direction, col - 1))
            if col + 1 < 8 and self.board[row + direction][col + 1].has_Enemy(piece.color):
                possible_moves.append((row + direction, col + 1))
            initial_move = Square(row, col)
            for possible_move in possible_moves:
                possible_row, possible_col = possible_move
                final_Piece = self.board[possible_row][possible_col].piece
                final_move = Square(possible_row, possible_col, final_Piece)
                move = (initial_move, final_move)
                if bool:
                    if not self.check_Checkmate(piece, move):
                        piece.add_Move(move)
                else:
                    piece.add_Move(move)
        def Knight_move():
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]
            initial_move = Square(row, col)
            for possible_move in possible_moves:
                possible_row, possible_col = possible_move
                if Square.in_range(possible_row, possible_col):                    
                    if self.board[possible_row][possible_col].is_empty_or_has_enemy(piece.color):
                        final_Piece = self.board[possible_row][possible_col].piece
                        final_move = Square(possible_row, possible_col, final_Piece)
                        move = (initial_move, final_move)
                        if bool:
                            if not self.check_Checkmate(piece, move):
                                piece.add_Move(move)
                        else:
                            piece.add_Move(move)                 
        def Rook_move():
            possible_moves = []
            dirs = [
                (1, 0),
                (-1, 0),
                (0, -1),
                (0, 1)
            ]
            for dir in dirs:
                for i in range(1, 8):
                    new_row = row + i * dir[0]
                    new_col = col + i * dir[1]
                    if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
                        if not self.board[new_row][new_col].has_Piece():
                            possible_moves.append((new_row, new_col))
                        elif self.board[new_row][new_col].has_Enemy(piece.color):
                            possible_moves.append((new_row, new_col))
                            break
                        else:
                            break
                    else:
                        break
            initial_move = Square(row, col)
            for possible_move in possible_moves:
                possible_row, possible_col = possible_move
                final_Piece = self.board[possible_row][possible_col].piece
                final_move = Square(possible_row, possible_col, final_Piece)
                move = (initial_move, final_move)
                if bool:
                    if not self.check_Checkmate(piece, move):
                        piece.add_Move(move)
                else:
                    piece.add_Move(move)   
            if bool:
                move = (initial_move, initial_move)
                if not self.check_Checkmate(piece, move):
                    if col == 7 and can_Castling_side_King():
                        final_Piece = self.board[row][col - 2].piece
                        final_move = Square(row, col - 2, final_Piece)
                        move = (initial_move, final_move)
                        if bool:
                            if not self.check_Checkmate(piece, move):
                                piece.add_Move(move)
                        else:
                            piece.add_Move(move)
                        
                    if col == 0 and can_Castling_side_Queen():
                        final_Piece = self.board[row][col + 3].piece
                        final_move = Square(row, col + 3, final_Piece)
                        move = (initial_move, final_move)
                        if bool:
                            if not self.check_Checkmate(piece, move):
                                piece.add_Move(move)
                        else:
                            piece.add_Move(move)
        def Bishop_move():
            possible_moves = []
            dirs = [
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1)
            ]
            for dir in dirs:
                for i in range(1, 8):
                    new_row = row + i * dir[0]
                    new_col = col + i * dir[1]
                    if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
                        if not self.board[new_row][new_col].has_Piece():
                            possible_moves.append((new_row, new_col))
                        elif self.board[new_row][new_col].has_Enemy(piece.color):
                            possible_moves.append((new_row, new_col))
                            break
                        else:
                            break
                    else:
                        break
            initial_move = Square(row, col)
            for possible_move in possible_moves:
                possible_row, possible_col = possible_move
                final_Piece = self.board[possible_row][possible_col].piece
                final_move = Square(possible_row, possible_col, final_Piece)
                move = (initial_move, final_move)
                if bool:
                    if not self.check_Checkmate(piece, move):
                        piece.add_Move(move)
                else:
                    piece.add_Move(move)
        def Queen_move():
            possible_moves = []
            dirs = [
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1),
                (1, 0),
                (-1, 0),
                (0, -1),
                (0, 1)
            ]
            for dir in dirs:
                for i in range(1, 8):
                    new_row = row + i * dir[0]
                    new_col = col + i * dir[1]
                    if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
                        if not self.board[new_row][new_col].has_Piece():
                            possible_moves.append((new_row, new_col))
                        elif self.board[new_row][new_col].has_Enemy(piece.color):
                            possible_moves.append((new_row, new_col))
                            break
                        else:
                            break
                    else:
                        break
            initial_move = Square(row, col)
            for possible_move in possible_moves:
                possible_row, possible_col = possible_move
                final_Piece = self.board[possible_row][possible_col].piece
                final_move = Square(possible_row, possible_col, final_Piece)
                move = (initial_move, final_move)
                if bool:
                    if not self.check_Checkmate(piece, move):
                        piece.add_Move(move)
                else:
                    piece.add_Move(move)
        def King_move():
            possible_moves = [
                (row + 1, col + 1),
                (row + 1, col - 1),
                (row - 1, col + 1),
                (row - 1, col - 1),
                (row + 1, col),
                (row, col + 1),
                (row - 1, col),
                (row, col - 1),
            ]
            initial_move = Square(row, col)
            for possible_move in possible_moves:
                possible_row, possible_col = possible_move
                if Square.in_range(possible_row, possible_col):                    
                    if self.board[possible_row][possible_col].is_empty_or_has_enemy(piece.color):
                        final_Piece = self.board[possible_row][possible_col].piece
                        final_move = Square(possible_row, possible_col, final_Piece)
                        move = (initial_move, final_move)
                        if bool:
                            if not self.check_Checkmate(piece, move):
                                piece.add_Move(move)
                        else:
                            piece.add_Move(move)
            if bool:
                move = (initial_move, initial_move)
                if not self.check_Checkmate(piece, move):
                    if can_Castling_side_King():
                        final_Piece = self.board[row][col + 2].piece
                        final_move = Square(row, col + 2, final_Piece)
                        move = (initial_move, final_move)
                        if bool:
                            if not self.check_Checkmate(piece, move):
                                piece.add_Move(move)
                        else:
                            piece.add_Move(move)
                    if can_Castling_side_Queen():
                        final_Piece = self.board[row][col - 2].piece
                        final_move = Square(row, col - 2, final_Piece)
                        move = (initial_move, final_move)
                        if bool:
                            if not self.check_Checkmate(piece, move):
                                piece.add_Move(move)
                        else:
                            piece.add_Move(move)

        if isinstance(piece, Pawn):
            Pawn_move()
        elif isinstance(piece, Rook):
            Rook_move()
        elif isinstance(piece, Knight):
            Knight_move()
        elif isinstance(piece, Bishop):
            Bishop_move()
        elif isinstance(piece, Queen):
            Queen_move()
        elif isinstance(piece, King):
            King_move()
    def create_Board(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = Square(row, col)
    
    def add_Piece(self, color):
        row_Pawn = 6 if color == 'White' else 1
        row_Other = 7 if color == 'White' else 0
        # Set pos of Pawns
        for col in range(COLS):
            self.board[row_Pawn][col] = Square(row_Pawn, col, Pawn(color))
        # # Set pos of Knights
        self.board[row_Other][1] = Square(row_Pawn, 1, Knight(color))
        self.board[row_Other][6] = Square(row_Pawn, 6, Knight(color))
        # # Set pos of Bishops
        self.board[row_Other][2] = Square(row_Pawn, 2, Bishop(color))
        self.board[row_Other][5] = Square(row_Pawn, 5, Bishop(color))
        # Set pos of Rooks
        self.board[row_Other][0] = Square(row_Pawn, 0, Rook(color))
        self.board[row_Other][7] = Square(row_Pawn, 7, Rook(color))
        # Set pos of Queens
        self.board[row_Other][3] = Square(row_Pawn, 3, Queen(color))
        # Set pos of Kings
        self.board[row_Other][4] = Square(row_Pawn, 4, King(color))

piece_square_tables = {
    "Pawn": [
        [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00],
        [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
        [0.07, 0.07, 0.08, 0.09, 0.09, 0.08, 0.07, 0.07],
        [0.03, 0.03, 0.05, 0.08, 0.08, 0.05, 0.03, 0.03],
        [0.02, 0.02, 0.04, 0.07, 0.07, 0.04, 0.02, 0.02],
        [0.01, 0.01, 0.03, 0.06, 0.06, 0.03, 0.01, 0.01],
        [0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    ],
    "Knight": [
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
        [0.00, 0.02, 0.06, 0.05, 0.05, 0.06, 0.02, 0.00],
        [0.00, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.00],
        [0.00, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.00],
        [0.00, 0.02, 0.06, 0.05, 0.05, 0.06, 0.02, 0.00],
        [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    ],
    "Bishop": [
        [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02],
        [0.01, 0.05, 0.03, 0.03, 0.03, 0.03, 0.05, 0.01],
        [0.01, 0.03, 0.07, 0.05, 0.05, 0.07, 0.03, 0.01],
        [0.01, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.01],
        [0.01, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.01],
        [0.01, 0.03, 0.07, 0.05, 0.05, 0.07, 0.03, 0.01],
        [0.01, 0.05, 0.03, 0.03, 0.03, 0.03, 0.05, 0.01],
        [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02],
    ],
    "Rook": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0.05, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.05],
        [0.05, 0, 0, 0, 0, 0, 0, 0.05],
        [0.05, 0, 0, 0, 0, 0, 0, 0.05],
        [0.05, 0, 0, 0, 0, 0, 0, 0.05],
        [0.05, 0, 0, 0, 0, 0, 0, 0.05],
        [0.05, 0, 0, 0, 0, 0, 0, 0.05],
        [0, 0, 0, 0.05, 0, 0.05, 0, 0]
    ],
    "Queen": [
        [0.2, 0.1, 0.1, 0.05, 0.05, 0.1, 0.1, 0.2],
        [0.1, 0, 0, 0, 0, 0, 0, 0.1],
        [0.1, 0, 0.05, 0.05, 0.05, 0.05, 0, 0.1],
        [0.05, 0, 0.05, 0.05, 0.05, 0.05, 0, 0.05],
        [0, 0, 0.05, 0.05, 0.05, 0.05, 0, 0.05],
        [0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0, 0.1],
        [0.1, 0, 0.05, 0, 0, 0, 0, 0.1],
        [0.1, 0.1, 0.1, 0.05, 0.05, 0.1, 0.1, 0.1]
    ],
    "King": [
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02],
        [0.05, 0.05, 0.10, 0.00, 0.00, 0.00, 0.10, 0.05],
    ]
}
