
import time
class Board:
    def __init__(self):
        self.board = self.create_board()
        self.castling_rights = {
            'wK': True, 'wQ': True,  # White King-side and Queen-side
            'bK': True, 'bQ': True   # Black King-side and Queen-side
        }
        # Stores the (r, c) tuple of the pawn that just moved two squares, or None
        self.en_passant_target = None
        # --- END NEW STATE VARIABLES ---

    def create_board(self):
        # Initialize an 9x8 board (8 rows for pieces, 1 row for algebraic labels)
        board = [['# ' for _ in range(8)] for _ in range(9)]
        
        specialrow = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        pawns = ['p' for _ in range(8)]

        # 1. Place Black pieces (Rank 8, Index 0)
        board[0] = ['b' + x for x in specialrow] 
        # 2. Place Black pawns (Rank 7, Index 1)
        board[1] = ['b' + j for j in pawns]
        
        # 3. Place White pawns (Rank 2, Index 6)
        board[6] = ['w' + n for n in pawns] 
        # 4. Place White pieces (Rank 1, Index 7)
        board[7] = ['w' + i for i in specialrow] 

        # --- (Your original label logic remains the same, assuming it's correct) ---
        navcol = ['a','b','c','d','e','f','g','h']
        navrow = [8,7,6,5,4,3,2,1]
        board[8] = [" " + n for n in navcol]
        for i in navrow:
            board[i-1].append(str(8-i+1)) 
        
        return board
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
        elif 'R' in piece:
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
                    ylaser = board[i+1][start[0]]
                    print(ylaser, i)
                    if ylaser[0] == piece[0]:
                        print("Can't hit your own pieces")
                        print(piece[0],ylaser[0])
                    else: legal = True 
                    if endpiece[0] != '#' and piece[0] != endpiece[0]:
                        attack = True
                    return legal, piece, attack
        elif 'N' in piece:
            print("Knight")
            if abs(xdiff) == 1 and abs(ydiff) == 2 and endpiece[0] != piece[0]:
                legal = True
                if endpiece[0] != '#':
                    attack = True
            elif abs(xdiff) == 2 and abs(ydiff) == 1 and endpiece[0] != piece[0]:
                legal = True
                if endpiece[0] != '#':
                    attack = True
        elif 'B' in piece[1]:
            if piece[0] == endpiece[0]:
                print("cant hit your own piece")
                return legal, piece, attack
            elif abs(xdiff) == abs(ydiff) and abs(xdiff) in [1,2,3,4,5,6,7,8]:
                legal = True
                if piece[0] in ['w','b'] and endpiece[0] in ['w''b'] and piece[0] != endpiece[0]:
                    attack = True
        elif 'Q' in piece[1]:
            if abs(xdiff) == abs(ydiff) and abs(xdiff) in [1,2,3,4,5,6,7,8]:
                legal = True
                if piece[0] in ['w','b'] and endpiece[0] in ['w''b'] and piece[0] != endpiece[0]:
                    attack = True
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
    # In Board.py:
    # In Board.py:
    def print_board(self):
        for row in self.board:
            # Create a new list of strings for printing
            printable_row = []
            for item in row:
                if isinstance(item, tuple):
                    # If it's a tuple (like ('wp', True)), use the piece symbol (item[0])
                    printable_row.append(item[0])
                else:
                    # If it's a string (like 'wR' or '# '), use the item itself
                    printable_row.append(item)
                    
            # Now join the list of strings
            print(' '.join(printable_row))
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
    
    # In Board.py, replace the existing make_move function:

    def make_move(self, start, end, piece):
        """
        Executes the move, updates the board state, and handles special moves 
        like CASTLING (moving the Rook).
        """
        board = self.board
        
        # 1. Check for Castling (King moves two squares horizontally)
        if 'K' in piece:
            xdiff = abs(start[0] - end[0]) # Should be 0 for castling
            ydiff = start[1] - end[1]      # Should be -2 or 2 for castling
            
            # Check if it's a castling move: King's row doesn't change, column changes by 2
            if xdiff == 0 and abs(ydiff) == 2:
                print("Executing Castling Move...")
                king_row = start[0]
                
                # King-side (Short) Castling: e1 -> g1 (ydiff = -2) or e8 -> g8
                if ydiff == -2: 
                    # Move King from col 4 to col 6 (handled below)
                    # Move Rook from col 7 to col 5
                    rook_piece = board[king_row][7]
                    board[king_row][5] = rook_piece
                    board[king_row][7] = '# '
                
                # Queen-side (Long) Castling: e1 -> c1 (ydiff = 2) or e8 -> c8
                elif ydiff == 2:
                    # Move King from col 4 to col 2 (handled below)
                    # Move Rook from col 0 to col 3
                    rook_piece = board[king_row][0]
                    board[king_row][3] = rook_piece
                    board[king_row][0] = '# '
                
                # NOTE: Castling logic for state update is handled further down

        # 2. Extract Piece Details and Update Pawn State (Existing Logic)
        piece_color = piece[0]
        piece_type = piece[1] if isinstance(piece, str) else piece[0][1] 

        # Handle Pawn state (first move to tuple)
        is_pawn_first_move = piece_type == 'p' and (
            piece_color == 'w' and start[0] == 6 or 
            piece_color == 'b' and start[0] == 1
        )
        
        if is_pawn_first_move and abs(start[0] - end[0]) == 2:
            board[end[0]][end[1]] = (piece, True)
        elif piece_type == 'p' and isinstance(piece, str) and abs(start[0] - end[0]) == 1:
            board[end[0]][end[1]] = (piece, True)
        else:
            board[end[0]][end[1]] = piece
            
        board[start[0]][start[1]] = '# ' # Clear the starting square (King or other piece)

        # 3. Update Castling Rights (Existing Logic)
        if piece_type == 'K':
            self.castling_rights[piece_color + 'K'] = False
            self.castling_rights[piece_color + 'Q'] = False
        elif piece == 'wR' and start == (7, 0): 
            self.castling_rights['wQ'] = False
        elif piece == 'wR' and start == (7, 7): 
            self.castling_rights['wK'] = False
        elif piece == 'bR' and start == (0, 0): 
            self.castling_rights['bQ'] = False
        elif piece == 'bR' and start == (0, 7): 
            self.castling_rights['bK'] = False
        
        # 4. Update En Passant Target (Existing Logic)
        self.en_passant_target = None 
        xdiff_pawn = abs(start[0] - end[0])
        if piece_type == 'p' and xdiff_pawn == 2:
            target_row = (start[0] + end[0]) // 2
            self.en_passant_target = (target_row, start[1])