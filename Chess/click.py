class Click:
    def __init__(self):
        self.piece = None
        self.row_idx = 0
        self.col_idx = 0
    def update_idx(self, piece, row, col):
        self.piece = piece
        self.col_idx = col
        self.row_idx = row