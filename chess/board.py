
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
        piece = self.board[start[0]][start[1]] #start[0] - Individual Sublist #start[1] position within Sublist
        endpiece = self.board[end[0]][end[1]] #end[0] - Individual sublist #start[1] position within sublist
        blackbools = [True for _ in range(8)] # for _ = placeholder. could be a-z, for when you just don't care enough.
        whitebools = [True for _ in range(8)]
        print(f"Start piece: {piece} End piece: {endpiece}")
        legal = False
        attack = False
        xdiff = start[0] - end[0]  
        ydiff = start[1] - end[1]
        print(f"Xdiff: {xdiff} Ydiff: {ydiff}")
        print(f"Start: {start} End: {end}")
        print(f"Start[0]: {start[0]}\nStart[1]:{start[1]}\nEnd[0]:{end[0]}\nEnd[1]:{end[1]}")
        print(f"Start tuple: {start}\nEnd tuple: {end}")
        if 'p' in piece: # pawn logic
            if 'w' in piece:
                whitebools[start[1]] = False #
                print(whitebools)
            elif 'b' in piece:
                blackbools[start[1]] = False
                print(blackbools)
            if turn: 
                if xdiff == -2 and ydiff == 0 and blackbools[start[1]] and endpiece[0] == '#': #* if pawn hasnt move they can move up twice
                    legal = True
                elif xdiff == -1 and ydiff == 0 and endpiece[0] == '#': #* if space is empty and white wants to move down one space 
                    legal = True
                elif xdiff == -1 and ydiff in [-1,1] and endpiece[0] == 'b': #* if white wants to move down and diagonal, the square must have an enemy
                    legal = True
                    attack = True
            elif turn == False: ## black turn
                if xdiff == 2 and ydiff == 0 and whitebools[start[1]] == True and endpiece[0] == '#':
                    legal = True
                elif xdiff == 1 and ydiff == 0 and endpiece[0] == '#':
                    legal = True
                elif xdiff == 1 and ydiff in [-1,1] and endpiece[0] == 'w':
                    legal = True
                    attack = True
                #! EN PASSANT 
        if 'R' in piece:
            if xdiff == 0: #* moving sideways
                for i in range(abs(ydiff)):
                    xlaser = board[start[0]][i+1]
                    print(xlaser, i)
                    if xlaser[0] == piece[0]:
                        print("Can't hit your own piece")
                        break
                    else: legal = True
                    attack = True 
                    return legal, piece, attack
            elif ydiff == 0:
                print("moving vertically")
                for i in range(abs(xdiff)):
                    ylaser = board[i+1][start[1]]
                    print(ylaser, i)
                    if ylaser[0] == piece[0]:
                        print("Can't hit your own pieces")
                        break
                    else: legal = True 
                    attack = True
                    return legal, piece, attack
        if 'N' in piece:
            print("Knight")
            if abs(xdiff) == 1 and abs(ydiff) == 2 and endpiece[0] != piece[0]:
                legal = True
                if endpiece[0] != '#':
                    attack = True
            elif abs(xdiff) == 2 and abs(ydiff) == 1 and endpiece[0] != piece[0]:
                legal = True
                if endpiece[0] != '#':
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
    def make_move(self,start,end,piece):
        board = self.board
        print("moving!")
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = '# '