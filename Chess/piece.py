class Piece:
    def __init__(self, name : str, color : str, value : int, texture = None, texture_rect = None) -> None:
        self.name = name
        self.color = color
        self.value = value if color == 'White' else -1 * value
        self.moves = []
        self.is_Moved = False
        self.texture = self.set_texture()
        self.texture_rect = texture_rect
    # Set texture
    def set_texture(self):
        return f'Image/{self.color}_{self.name}.png'
    # Add move
    def add_Move(self, move):
        self.moves.append(move)
class Pawn(Piece):
    def __init__(self, color : str):
        self.dir = 1 if color == 'White' else -1
        super().__init__('Pawn', color, 1)

class Knight(Piece):
    def __init__(self, color : str):
        super().__init__('Knight', color, 3)

class Bishop(Piece):
    def __init__(self, color : str):
        super().__init__('Bishop', color, 3)

class Rook(Piece):
    def __init__(self, color : str):
        super().__init__('Rook', color, 3)

class Queen(Piece):
    def __init__(self, color : str):
        super().__init__('Queen', color, 10)

class King(Piece):
    def __init__(self, color : str):
        super().__init__('King', color, 9999)