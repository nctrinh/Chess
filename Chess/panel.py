import time
import pygame
import sys

from constaints import *
from UI import UI
from board import *
from click import Click
from AI import *

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
        self.AI = AI(3, "Black")
        self.game_Mode = 'PvA'
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
            self.game_Board.check_State(self, self.turn)
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
                            if self.game_Board.board[row_idx][col_idx].piece != selected_Piece and self.game_Board.board[row_idx][col_idx].has_Team(self.turn):
                                self.game_Board.calc_moves(chosen_Piece, clicked_Row, clicked_Col, True)                        
                                possible_Moves = chosen_Piece.moves           
                                self.click.update_idx(chosen_Piece, clicked_Row, clicked_Col)
                                selected_Piece = chosen_Piece
                            else:
                                for move in possible_Moves:
                                    initial_move, final_move = move[0], move[1]              
                                    if row_idx == final_move.row_idx and col_idx == final_move.col_idx:
                                        self.game_Board.move_Piece(selected_Piece, move)
                                        self.turn = 'White' if self.turn == 'Black' else 'Black'
                                        selected_Piece = None
                                        possible_Moves = []                                    
                                        if self.game_Mode == "PvA":
                                            self.UI.show_Board(self.screen)           
                                            self.UI.show_Pieces(self.screen)   
                                            pygame.display.update()                             
                                            move = self.AI.eval(self.game_Board, self.turn)
                                            if move:
                                                initail_move, final_move = move[0], move[1]
                                                piece = self.game_Board.board[initail_move.row_idx][initail_move.col_idx].piece
                                                self.game_Board.move_Piece(piece, move)
                                                self.turn = 'White' if self.turn == 'Black' else 'Black'
                                        break 
                                selected_Piece = None   
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:   
                           if self.game_Mode == "PvA":
                                self.UI.show_Board(self.screen)           
                                self.UI.show_Pieces(self.screen)   
                                pygame.display.update()                             
                                move = self.AI.eval(self.game_Board, self.turn)
                                if move:
                                    initail_move, final_move = move[0], move[1]
                                    piece = self.game_Board.board[initail_move.row_idx][initail_move.col_idx].piece
                                    self.game_Board.move_Piece(piece, move)
                                    self.turn = 'White' if self.turn == 'Black' else 'Black'                      
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            else:
                self.UI.show_End(self.screen, self.state, self.turn)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.game_Board = Board()
                            self.click = Click()
                            self.UI = UI(self.game_Board, self.click)
                            self.choose_Piece = False
                            self.choosen_Piece = None
                            self.turn = "White"
                            self.state = 'Playing'
                            print("reset")
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
    # Start game
    def game_Start(self):
        self.game_Loop()

