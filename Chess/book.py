from node import Node
from board import Square
class Book:
    def __init__(self):
        self.head = Node()
        self._create_Tree()
    def find_Move(self, moves, weighted = True):
        for i, move in enumerate(moves):
            if i == 0: 
                node = self.head
            for child in node.children:
                if move[0].row_idx == child.move[0].row_idx and move[0].col_idx == child.move[0].col_idx and move[1].row_idx == child.move[1].row_idx and move[1].col_idx == child.move[1].col_idx:
                    if len(moves)-1 == i:
                        move = child.choose_child(weighted)
                        return move.move
                    else:
                        node = child
    def _create_Tree(self):
        # 1
        self.head.add_Children(
            Node((Square(6, 4), Square(4, 4)), 1000),
            Node((Square(6, 3), Square(4, 3)), 1000),
            Node((Square(7, 6), Square(5, 5)), 1000),
            Node((Square(6, 2), Square(4, 2)), 1000),
            Node((Square(6, 4), Square(5, 4)), 1000),
            Node((Square(6, 6), Square(5, 6)), 1000),
            Node((Square(6, 1), Square(5, 1)), 1000),
            Node((Square(6, 5), Square(4, 5)), 1000),            
            Node((Square(6, 3), Square(5, 3)), 1000),
            Node((Square(7, 1), Square(5, 2)), 1000),
            Node((Square(6, 1), Square(4, 1)), 1000),
            Node((Square(6, 2), Square(5, 2)), 1000),
        )
        for i in range(12):
            self.head.children[i].add_Children(
                Node((Square(1, 4), Square(3, 4)), 1000),  # 1... e5 (King's Pawn Game)
                Node((Square(1, 2), Square(3, 2)), 1000),  # 1... c5 (Sicilian Defense)
                Node((Square(1, 3), Square(3, 3)), 1000),  # 1... d5 (Scandinavian Defense)
                Node((Square(1, 4), Square(2, 4)), 1000),  # 1... e6 (French Defense)
                Node((Square(1, 2), Square(2, 2)), 1000),  # 1... c6 (Caro-Kann Defense)
                Node((Square(1, 3), Square(2, 3)), 1000),  # 1... d6 (Pirc Defense)
                Node((Square(1, 6), Square(2, 6)), 1000),  # 1... g6 (Modern Defense)
                Node((Square(1, 1), Square(2, 1)), 1000),  # 1... b6 (Owen Defense)
                Node((Square(0, 6), Square(2, 5)), 1000),  # 1... Nf6 (Alekhine Defense)
                Node((Square(0, 1), Square(2, 2)), 1000),  # 1... Bb6 (Biến thể)
                Node((Square(1, 0), Square(2, 0)), 1000),  # 1... a6 (St. George Defense)
                Node((Square(1, 5), Square(3, 5)), 1000),  # 1... f5 (Duras Gambit)
            )
        # self.head.children[0].children[0].add_Children(
        #     Node(((7, 6), (5, 5)), 1000),  # 2. Nf3 (King's Knight Opening)
        #     Node(((7, 5), (4, 2)), 1000),  # 2. Bc4 (Bishop's Opening)
        #     Node(((7, 6), (5, 4)), 1000),  # 2. Nc3 (Vienna Game)
        #     Node(((6, 3), (4, 3)), 1000),  # 2. d4 (Center Game)
        #     Node(((6, 5), (4, 5)), 1000),  # 2. f4 (King's Gambit)
        #     Node(((6, 2), (4, 2)), 1000),  # 2. c3 (MacLeod Attack)
        #     Node(((6, 2), (4, 4)), 1000),  # 2. c4 (English Opening)
        #     Node(((7, 3), (5, 7)), 1000),  # 2. Qh5 (Wayward Queen Attack)
        #     Node(((7, 3), (5, 5)), 1000),  # 2. Qf3 (Napoleon Attack)
        #     Node(((6, 3), (5, 3)), 1000),  # 2. d3 (Leonardis Variation)
        #     Node(((7, 5), (5, 5)), 1000),  # 2. f3 (King's Head Opening)
        #     Node(((7, 5), (5, 6)), 1000),  # 2. g3 (Grob's Attack)
        # )
        
        