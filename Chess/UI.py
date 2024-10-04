import pygame 
from click import Click
from constaints import *
from board import *

class UI:
    def __init__(self, game_Board : Board, click : Click):
        self.game_Board = game_Board
        self.click = click

    def show_Board(self, surface : pygame.Surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (col + row) % 2 == 0:
                    color_Code = '#806640'
                else:
                    color_Code = '#332313'
                pygame.draw.rect(surface, color_Code, (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE))
    
    def show_Pieces(self, surface : pygame.Surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.game_Board.board[row][col].has_Piece():
                    piece = self.game_Board.board[row][col].piece
                    piece_Img = pygame.image.load(piece.texture)
                    piece_Center = col * SQSIZE + SQSIZE / 2, row * SQSIZE + SQSIZE / 2
                    piece.texture_rect = piece_Img.get_rect(center = piece_Center)
                    surface.blit(piece_Img, piece.texture_rect)
    
    def show_Moves(self, surface : pygame.Surface):
        if self.click.piece:
            piece = self.click.piece
            for move in piece.moves:
                color = '#C84646' if (move[1].row_idx + move[1].col_idx) % 2 == 0 else '#C86464'
                rect = (move[1].col_idx * SQSIZE, move[1].row_idx * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_Last_Move(self, surface : pygame.Surface):
        last_Move = self.game_Board.last_Move
        if last_Move:
            for move in last_Move:
                move_col_idx, move_row_idx= move.col_idx, move.row_idx
                color = '#006600' if (move_col_idx + move_row_idx) % 2 == 0 else '#007700'
            
                rect = (move_col_idx * SQSIZE, move_row_idx * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
            