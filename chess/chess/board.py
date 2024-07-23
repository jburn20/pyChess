class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [['# ' for _ in range(8)] for _ in range(8)]
        # ^ create board, now we can modify with board[] statements 
        # Initialize the board with pieces
        specialrow = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        pawns = ['p' for _ in range(8)]
        board[0] = ['w' + x for x in specialrow] # we can set our bottom and top rows to have special rows
        board[1] = ['w' + j for j in pawns]
        board[7] = ['b' + i for i in specialrow] ## iteration
        board[6] = ['b' + n for n in pawns]
        return board
    def print_board(self):
        for row in self.board:
            print(' '.join(row)) # Board is a list of 8 sublists with each list containing 1 row.
        print()

    def coord_converter(self,coord):
        column, row = coord
        col_index = ord(column) - ord("a")
        row_index = 8 - int(row)
        return (row_index,col_index)
    def get_move(self):
        move = input("Make your move: ")
        x,y = move.split()
        return self.coord_converter(x), self.coord_converter(y)
    
    def is_valid(self,start,end):
        piece = self.board[start[0]][start[1]]
        desire = self.board[end[0]][end[1]]
        empty = '#'
        print(desire)
        if empty in desire:
            print("clear")
        if 'p' in piece:
            print("pawn")
        if 'R' in piece:
            print("rook")
    def make_move(self,start,end):
        pass
"""
1. Move validation:
-- Find piece with .is_valid()
-- Implement logic such as pawn cannot move farther than 1 space
2. Move logic
3. Update board with move logic
"""
    
    
    
        