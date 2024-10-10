import random
from board import *

class Node:

    def __init__(self, turn, board : Board) -> None:
        self.board = board
        self.value = board.evaluate(turn)
        self.prob = 0
        self.children = []
    
    def add_Child(self, child):
        self.children.append(child)

    def calc_prob(self):
        total_value = 0
        for child in self.children:
            total_value += child.value
        
        for child in self.children:
            child.prob = (child.value / total_value) * 100

    def choose_child(self, prob = False):
        if not prob:
            max_Node = self.children[0]
            for node in self.children:
                if node.value > max_Node.value:
                    max_Node = node
            return max_Node
        else:
            rnd = random.randint(1, 100)
            c = 0
            for node in self.children:
                if rnd <= node.prob + c:
                    return node        
                c += node.prob