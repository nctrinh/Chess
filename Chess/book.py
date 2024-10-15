from node import Node
from board import Square
class Book:
    def __init__(self):
        self.head = Node()
        self._create_Tree()
    def find_Move(self, moves, weighted = True):       
        if moves[0] == None and len(moves) == 1:
            moves[0] = self.head.choose_child(weighted).move 
            return moves[0]
        for i, move in enumerate(moves):
            if i == 0: 
                node = self.head
            for child in node.children:                   
                if move[0].row_idx == child.move[0].row_idx and move[0].col_idx == child.move[0].col_idx and move[1].row_idx == child.move[1].row_idx and move[1].col_idx == child.move[1].col_idx:
                    if len(moves)-1 == i:
                        move = child.choose_child(weighted)
                        if move:
                            return move.move
                    else:
                        node = child
    def _create_Tree(self):
        # 1
        self.head.add_Children(
            Node((Square(6, 4), Square(4, 4)), 3222121), # e4
            Node((Square(6, 3), Square(4, 3)), 1390000), # d4
            Node((Square(7, 6), Square(5, 5)), 190800), # nf3
            Node((Square(6, 2), Square(4, 2)), 184300), # c4
            Node((Square(6, 4), Square(5, 4)), 112500), # e3
        )
        #2
        self.head.children[0].add_Children(
            Node((Square(1, 4), Square(3, 4)), 1289500), # e5
            Node((Square(1, 2), Square(3, 2)), 600000), # c5
            Node((Square(1, 3), Square(3, 3)), 333000), # d5
            Node((Square(1, 4), Square(2, 4)), 331000), # e6
        )
        self.head.children[1].add_Children(
            Node((Square(1, 3), Square(3, 3)), 573000), # d5
            Node((Square(0, 6), Square(2, 5)), 273000), # nf6
            Node((Square(1, 4), Square(2, 4)), 138000), # e6
            Node((Square(1, 4), Square(3, 4)), 82000), # e5           
        )
        self.head.children[2].add_Children(
            Node((Square(1, 3), Square(3, 3)), 61000), # d5
            Node((Square(0, 6), Square(2, 5)), 29000), # nf6
            Node((Square(1, 2), Square(3, 2)), 18000), # c5
            Node((Square(1, 4), Square(2, 4)), 17000), # e6
        )
        self.head.children[3].add_Children(
            Node((Square(1, 4), Square(3, 4)), 54000), # e5 
            Node((Square(0, 6), Square(2, 5)), 30000), # nf6
            Node((Square(1, 2), Square(3, 2)), 21000), # c5
            Node((Square(1, 4), Square(2, 4)), 20000), # e6
        )
        self.head.children[4].add_Children(
            Node((Square(1, 4), Square(3, 4)), 40000), # e5 
            Node((Square(1, 3), Square(3, 3)), 22000), # d5
            Node((Square(1, 2), Square(3, 2)), 11000), # c5
            Node((Square(1, 4), Square(2, 4)), 10000), # e6
        )
        # 3
        self.head.children[0].children[0].add_Children(
            Node((Square(7, 6), Square(5, 5)), 794000), # nf3
            Node((Square(7, 5), Square(4, 2)), 132000), # bc4
        )
        self.head.children[0].children[1].add_Children(
            Node((Square(7, 6), Square(5, 5)), 319000), # nf3
            Node((Square(7, 1), Square(5, 2)), 58000), # nc3
        )
        self.head.children[1].children[0].add_Children(
            Node((Square(6, 2), Square(4, 2)), 226000), # c4
            Node((Square(7, 2), Square(4, 5)), 102000), # bf4
        )
        self.head.children[1].children[1].add_Children(
            Node((Square(6, 2), Square(4, 2)), 115000), # c4
            Node((Square(7, 6), Square(5, 5)), 52000), # nf3
        )
        self.head.children[2].children[0].add_Children(
            Node((Square(6, 3), Square(4, 3)), 20000), # d4
            Node((Square(6, 6), Square(5, 6)), 14000), # g3
        )
        self.head.children[2].children[1].add_Children(
            Node((Square(6, 6), Square(5, 6)), 9000), # g3
            Node((Square(6, 3), Square(4, 3)), 8000), # d4
        )
        self.head.children[3].children[0].add_Children(
            Node((Square(7, 1), Square(5, 2)), 32000), # nc3
            Node((Square(6, 6), Square(5, 6)), 7000), # g3
        )
        self.head.children[3].children[1].add_Children(
            Node((Square(7, 1), Square(5, 2)), 18000), # nc3
            Node((Square(6, 6), Square(5, 6)), 4000), # g3
        )
        self.head.children[4].children[0].add_Children(
            Node((Square(6, 3), Square(4, 3)), 8000), # d4
            Node((Square(6, 1), Square(5, 1)), 4000), # b3
        )
        self.head.children[4].children[1].add_Children(
            Node((Square(6, 3), Square(4, 3)), 6000), # d4
            Node((Square(6, 1), Square(5, 1)), 2000), # b3
        )
        #4
        self.head.children[0].children[0].children[0].add_Children(
            Node((Square(0, 1), Square(2, 2)), 500000), # nc6
        )
        self.head.children[0].children[0].children[1].add_Children(
            Node((Square(0, 6), Square(2, 5)), 43000), # nf6
        )
        self.head.children[0].children[1].children[0].add_Children(
            Node((Square(0, 1), Square(2, 2)), 133000), # nc6
        )
        self.head.children[0].children[1].children[1].add_Children(
            Node((Square(0, 1), Square(2, 2)), 25000), # nc6
        )

        self.head.children[1].children[0].children[0].add_Children(
            Node((Square(1, 4), Square(2, 4)), 10000), # e6
        )
        self.head.children[1].children[0].children[1].add_Children(
            Node((Square(0, 6), Square(2, 5)), 43000), # nf6    
        )
        self.head.children[1].children[1].children[0].add_Children(
            Node((Square(1, 4), Square(2, 4)), 10000), # e6
        )
        self.head.children[1].children[1].children[1].add_Children(
            Node((Square(1, 6), Square(2, 6)), 6000), # g6
        )

        self.head.children[2].children[0].children[0].add_Children(
            Node((Square(0, 6), Square(2, 5)), 43000), # nf6
        )
        self.head.children[2].children[0].children[1].add_Children(
            Node((Square(0, 6), Square(2, 5)), 43000), # nf6
        )
        self.head.children[2].children[1].children[0].add_Children(
            Node((Square(1, 6), Square(2, 6)), 6000), # g6
        )
        self.head.children[2].children[1].children[1].add_Children(
            Node((Square(1, 6), Square(2, 6)), 6000), # g6
        )

        self.head.children[3].children[0].children[0].add_Children(
            Node((Square(0, 6), Square(2, 5)), 43000), # nf6
        )
        self.head.children[3].children[0].children[1].add_Children(
            Node((Square(0, 6), Square(2, 5)), 43000), # nf6
        )
        self.head.children[3].children[1].children[0].add_Children(
            Node((Square(1, 6), Square(2, 6)), 6000), # g6
        )
        self.head.children[3].children[1].children[1].add_Children(
            Node((Square(1, 6), Square(2, 6)), 6000), # g6
        )
        
        self.head.children[4].children[0].children[0].add_Children(
            Node((Square(3, 4), Square(4, 3)), 6000), # exd4
        )
        self.head.children[4].children[0].children[1].add_Children(
            Node((Square(1, 3), Square(3, 3)), 22000), # d5
        )
        self.head.children[4].children[1].children[0].add_Children(
            Node((Square(0, 6), Square(2, 5)), 43000), # nf6
        )
        self.head.children[4].children[1].children[1].add_Children(
            Node((Square(1, 4), Square(3, 4)), 54000), # e5 
        )
        