
import time
class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [['# ' for _ in range(8)] for _ in range(9)] #first range - len of individual list | second range - num# of lists
        # ^ create board, now we can modify with board[] statements 
        # Initialize the board with pieces
        navcol = ['a','b','c','d','e','f','g','h']
        navrow = [8,7,6,5,4,3,2,1]
        board[8] = [" " + n for n in navcol]
        specialrow = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        pawns = ['p' for _ in range(8)]
        board[0] = ['w' + x for x in specialrow] # we can set our bottom and top rows to have special rows
        board[1] = ['w' + j for j in pawns]
        board[7] = ['b' + i for i in specialrow] ## iteration
        board[6] = ['b' + n for n in pawns]
        for i in navrow:
            board[i-1].append(str(8-i+1))
        
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
    
    def is_valid(self,start,end,turn:bool):
        board = self.board
        piece = self.board[start[0]][start[1]]
        endpiece = self.board[end[0]][end[1]]
        blackbools = [True for _ in range(8)]
        whitebools = [True for _ in range(8)]
        print(f"Start piece: {piece} End piece: {endpiece}")
        legal = False
        attack = False
        empty = '#'
        xdiff = start[0] - end[0]  
        ydiff = start[1] - end[1]
        print(f"Xdiff: {xdiff} Ydiff: {ydiff}")
        print(f"Start: {start} End: {end}")
        if 'p' in piece: # pawn logic
            if 'w' in piece:
                whitebools[start[1]] = False
                print(whitebools)
            elif 'b' in piece:
                blackbools[start[1]] = False
                print(blackbools)
            if turn == False:
                if xdiff == 2 and ydiff == 0 and whitebools[start[1]] == True:
                    legal = True
                elif xdiff == 1 and ydiff == 0:
                    legal = True
                elif endpiece not in empty and xdiff == 1 and ydiff in [-1,1]:
                    legal = True
            elif turn:
                if xdiff == -2 and ydiff == 0 and blackbools[start[1]]:
                    legal = True
                elif xdiff == -1 and ydiff == 0:
                    legal = True
                #elif 
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
    def switch_turn(self, turn:bool):
        if turn:
            turn = False
        else: turn = True
        return turn
        print("switched")
    def make_move(self,start,end,piece):
        board = self.board
        print("moving!")
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = '# '


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
    
    
    
        