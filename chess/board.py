
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
    # In Board.py, inside the Board class:

    def alg_to_coord(self, alg_coord):
        """
        Converts algebraic notation (e.g., 'e2') to internal (row, col) coordinates (e.g., (6, 4)).
        """
        if len(alg_coord) != 2:
            raise ValueError("Invalid algebraic coordinate format.")
            
        file = alg_coord[0].lower() # a-h
        rank = alg_coord[1]         # 1-8

        # File to Column: 'a' -> 0, 'h' -> 7
        col = ord(file) - ord('a')
        
        # Rank to Row: '1' -> 7, '8' -> 0 (Flipped board)
        row = 8 - int(rank)
        
        if not (0 <= row < 8 and 0 <= col < 8):
            raise IndexError("Coordinates are outside the board boundaries.")

        return (row, col)
# In Board.py, inside the Board class:

    def coord_to_alg(self, coord):
        """
        Converts internal (row, col) coordinates (e.g., (6, 4)) back to algebraic notation (e.g., 'e2').
        """
        row, col = coord
        
        # Column to File: 0 -> 'a', 7 -> 'h'
        file = chr(ord('a') + col)
        
        # Row to Rank: 7 -> '1', 0 -> '8'
        rank = str(8 - row)
        
        return file + rank
    def get_raw_input(self):
        """Prompts the user and returns the raw string input."""
        # Note: Using input() here will pause the execution until the user responds.
        return input("Make your move (e.g., e2 e4) or type 'moves': ").strip()
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