import pygame
import sys

from constaints import *
from UI import UI
from board import *
from click import Click

# Icon image
icon_Image = pygame.image.load(r'D:\projects\INT3401\Chess\Image\icon.jpg')

class Panel:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_icon(icon_Image)
        pygame.display.set_caption('Chess')
        self.game_Board = Board()
        self.click = Click()
        self.UI = UI(self.game_Board, self.click)
        self.choose_Piece = False
        self.choosen_Piece = None
        self.turn = "White"
        self.state = 'Playing'
    # Game loop
    def game_Loop(self):    
        selected_Piece = None
        possible_Moves = []
        while True:
            # Draw board
            self.UI.show_Board(self.screen)           
            self.UI.show_Last_Move(self.screen)
            if selected_Piece != None:
                self.UI.show_Moves(self.screen)
            self.UI.show_Pieces(self.screen)  
            if self.game_Board.has_valid_move(self.turn):         
                self.state = 'Playing'
            elif not self.game_Board.check_Checkmate_Now(self.turn):
                self.state = 'Draw'               
                print("Draw")
            else:
                self.state = 'End'
                print(f'{self.turn} lose')   
            if self.state == 'Playing':                   
                for event in pygame.event.get():                   
                    # Click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_PosX, mouse_PosY = event.pos
                        clicked_Row = int(mouse_PosY // SQSIZE)
                        clicked_Col = int(mouse_PosX // SQSIZE)
                        chosen_Square = self.game_Board.board[clicked_Row][clicked_Col]                         
                        chosen_Piece = chosen_Square.piece                   
                        if selected_Piece is None:    
                            if chosen_Piece != None:
                                if chosen_Piece.color == self.turn:
                                    self.game_Board.calc_moves(chosen_Piece, clicked_Row, clicked_Col, True)                        
                                    possible_Moves = chosen_Piece.moves           
                                    self.click.update_idx(chosen_Piece, clicked_Row, clicked_Col)
                                    selected_Piece = chosen_Piece
                        else:
                            self.click.update_idx(chosen_Piece, clicked_Row, clicked_Col)
                            row_idx, col_idx = self.click.row_idx, self.click.col_idx  
                            for move in possible_Moves:
                                initial_move, final_move = move[0], move[1]              
                                if row_idx == final_move.row_idx and col_idx == final_move.col_idx:
                                    self.game_Board.move_Piece(selected_Piece, move)
                                    self.turn = 'White' if self.turn == 'Black' else 'Black'
                                    selected_Piece = None
                                    possible_Moves = []
                                    break 
                            selected_Piece = None                                          
                    elif event.type == pygame.MOUSEBUTTONUP:
                        last_Piece = chosen_Piece
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
    # Start game
    def game_Start(self):
        self.game_Loop()

