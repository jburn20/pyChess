import time

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
            print(' '.join(row))
            time.sleep(0.09)
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
    
    def is_valid(self,start,end,):
        board = self.board
        piece = self.board[start[0]][start[1]]
        endpiece = self.board[end[0]][end[1]]
        print(f"Start piece: {piece} End piece: {endpiece}")
        legal = False
        attack = False
        empty = '#'
        xdiff = start[0] - end[0]  
        ydiff = start[1] - end[1]
        print(f"Xdiff: {xdiff} Ydiff: {ydiff}")
        print(f"Start: {start} End: {end}")
        if 'p' in piece:
            print("pawn")
            if xdiff == 1 and ydiff == 0 and empty in endpiece:
                legal = True
        if 'R' in piece:
            print("rook")
            for i in range(8):
                vert = board[i][start[0]]
                if vert not in empty:
                    attack = True
                
        return legal,piece ,attack

        """
        !!!!!
        MOVEMENT LOGIC HERE
        !!!!!
        """
    def make_move(self,start,end,piece):
        board = self.board
        print("moving!")
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = '#'


    def move_checker(self,move,piece):
        #### placeholder for validity functions
        # eventually this function will intake an attack or move function
        # if function is attack, we will check if it is aiming at a King (and put the game into check if so)
        # else we just replace first piece with  second piece
        board = self.board
        specialrow = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        pawns = ['p' for _ in range(8)]
        for i in range(8):
            vert = board[i][move[0]]
            if vert == '#':
                pass # pass on through empty space, redundant code
            if vert in pawns or vert in specialrow:
                print("Hit")
        
"""
1. Move validation:
-- Find piece with .is_valid()
-- Implement logic such as pawn cannot move farther than 1 space
2. Move logic
3. Update board with move logic
"""
    
    
    
        