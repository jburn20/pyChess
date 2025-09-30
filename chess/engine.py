from board import Board
class ChessEngine(Board):
    def __init__(self):
        super().__init__()
        self.castling_rights = {
            'wK': True, 'wQ': True, 'bK': True, 'bQ': True
        }
        self.en_passant_target = None
    def sync_board(self, board_instance):
        """Deep copy board and state from the main Board instance."""
        # Deep copy the board's 8x8 logical part (ignore labels)
        self.board = [row[:] for row in board_instance.board[:8]] 
        
        # Deep copy the state variables
        self.castling_rights = board_instance.castling_rights.copy()
        self.en_passant_target = board_instance.en_passant_target
    def apply_move(self, start, end):
        """
        Applies a pseudo-legal move to the internal board and records state for undo.
        Now includes special move handling for Castling and En Passant.
        """
        piece = self.board[start[0]][start[1]]
        
        # Determine piece details
        piece_color = piece[0] if isinstance(piece, str) else piece[0][0]
        piece_type = piece[1] if isinstance(piece, str) else piece[0][1] 
        
        # 1. CAPTURE STATE FOR UNDO
        state_backup = {
            'captured_piece': self.board[end[0]][end[1]],
            'prev_castling_rights': self.castling_rights.copy(), # Deep copy mutable dict
            'prev_en_passant_target': self.en_passant_target,
            'piece_moved_was_string': isinstance(piece, str), 
            'special_flag': None, # To track castling and en passant execution
        }
        
        # --- Special Move Pre-Move Checks ---
        ydiff = start[1] - end[1]

        # Check for En Passant Capture (before moving the piece)
        if piece_type == 'p' and end == self.en_passant_target:
            # Captured piece is on the start row, end col
            captured_pawn_pos = (start[0], end[1]) 
            state_backup['captured_piece'] = self.board[captured_pawn_pos[0]][captured_pawn_pos[1]]
            self.board[captured_pawn_pos[0]][captured_pawn_pos[1]] = '# ' # Remove the captured pawn
            state_backup['special_flag'] = 'EP_CAPTURE'

        # 2. UPDATE BOARD POSITION & PAWN STATE (Standard Move)
        
        # Update pawn representation to tuple if it was a string
        if piece_type == 'p' and isinstance(piece, str):
            self.board[end[0]][end[1]] = (piece, True)
        else:
            self.board[end[0]][end[1]] = piece
                
        self.board[start[0]][start[1]] = '# ' # Clear starting square

        # 3. SPECIAL MOVE EXECUTION: Castling (Move the Rook)
        if piece_type == 'K' and abs(ydiff) == 2:
            king_row = start[0]
            
            if ydiff == -2: # King-side (Short) Castling: e to g
                rook_piece = self.board[king_row][7]
                self.board[king_row][5] = rook_piece
                self.board[king_row][7] = '# '
                state_backup['special_flag'] = 'K_CASTLE'
            
            elif ydiff == 2: # Queen-side (Long) Castling: e to c
                rook_piece = self.board[king_row][0]
                self.board[king_row][3] = rook_piece
                self.board[king_row][0] = '# '
                state_backup['special_flag'] = 'Q_CASTLE'
                
        # 4. UPDATE CASTLING RIGHTS
        if piece_type == 'K':
            self.castling_rights[piece_color + 'K'] = False
            self.castling_rights[piece_color + 'Q'] = False
        elif piece_type == 'R':
            if start == (7, 0): self.castling_rights['wQ'] = False
            elif start == (7, 7): self.castling_rights['wK'] = False
            elif start == (0, 0): self.castling_rights['bQ'] = False
            elif start == (0, 7): self.castling_rights['bK'] = False

        # 5. UPDATE EN PASSANT TARGET
        self.en_passant_target = None # Reset
        if self._is_pawn_double_push(start, end, piece_type):
            target_row = (start[0] + end[0]) // 2 
            self.en_passant_target = (target_row, start[1])
                
        return state_backup
    def internal_board(self):
        """Return 8x8 logical board ignoring labels for calculations."""
        return [row[:8] for row in self.board[:8]]

    # In ChessEngine.py, inside the ChessEngine class:

    def undo_move(self, start, end, state_backup):
        """
        Reverses the move using the state backup, including special moves (Castling, En Passant).
        """
        # 1. Restore piece positions and captured piece
        piece_moved = self.board[end[0]][end[1]]
        
        # Logic to handle restoring the pawn state (from tuple back to string)
        is_pawn_to_restore = False
        
        # Check if the piece at the end position is a tuple and was originally a string
        if isinstance(piece_moved, tuple):
            # piece_moved[0] is the piece symbol string (e.g., 'wp')
            piece_symbol = piece_moved[0] 
            
            # Check if it's a pawn AND if the backup says it was originally a string
            if piece_symbol[1] == 'p' and state_backup['piece_moved_was_string']:
                is_pawn_to_restore = True
                
        if is_pawn_to_restore:
            # Restore the original string representation, e.g., 'wp'
            self.board[start[0]][start[1]] = piece_symbol 
        else:
            # Restore as is (either string, tuple, or '# ')
            self.board[start[0]][start[1]] = piece_moved

        # Restore the captured piece/empty square at the end position
        self.board[end[0]][end[1]] = state_backup['captured_piece']
        
        # 2. Restore global state
        self.castling_rights = state_backup['prev_castling_rights']
        self.en_passant_target = state_backup['prev_en_passant_target']

        # 3. SPECIAL MOVE UNDO: Castling (Move the Rook back)
        if state_backup['special_flag'] == 'K_CASTLE':
            king_row = start[0]
            # Move Rook back from col 5 to col 7
            rook_piece = self.board[king_row][5]
            self.board[king_row][7] = rook_piece
            self.board[king_row][5] = '# '

        elif state_backup['special_flag'] == 'Q_CASTLE':
            king_row = start[0]
            # Move Rook back from col 3 to col 0
            rook_piece = self.board[king_row][3]
            self.board[king_row][0] = rook_piece
            self.board[king_row][3] = '# '
            
        # 4. SPECIAL MOVE UNDO: En Passant (Restore the captured pawn)
        elif state_backup['special_flag'] == 'EP_CAPTURE':
            # The captured pawn was removed from the target's column, but the start row
            captured_pawn_pos = (start[0], end[1]) 
            self.board[captured_pawn_pos[0]][captured_pawn_pos[1]] = state_backup['captured_piece']

    def get_king_pos(self, color):
        """
        Finds and returns the (r, c) coordinates of the King of the given color.
        """
        king_symbol = color + 'K'
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                # King is always represented as a string
                if piece == king_symbol:
                    return (r, c)
        return None # Should not happen in a valid game state

    def is_in_check(self, color):
        """
        Checks if the King of the specified color is currently under attack.
        Relies on the already implemented is_square_attacked.
        """
        king_pos = self.get_king_pos(color)
        if king_pos is None:
            # This occurs if the King has been captured (i.e., checkmate occurred on the previous move)
            # For the purpose of the engine search, if the King is gone, we'll treat it as safe 
            # (the move that caused the capture would have been filtered by the opponent's check logic).
            return False
            
        kr, kc = king_pos
        attacker_color = 'b' if color == 'w' else 'w'
        
        # Check if the square the King is on is attacked by the opponent color
        return self.is_square_attacked(kr, kc, attacker_color)

    def is_square_attacked(self, r, c, attacker_color):
        """
        Checks if the square (r, c) is attacked by any piece of attacker_color.
        This is used for King safety checks (e.g., Castling and Check).
        """
        
        # Define the opponent color for clarity
        target_color = 'w' if attacker_color == 'b' else 'b'

        # --- 1. Check for Knight Attacks ---
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            pr, pc = r + dr, c + dc # Potential attacker position (pr, pc)
            if 0 <= pr < 8 and 0 <= pc < 8:
                piece = self.board[pr][pc]
                # Check for Knight piece (N) of the correct attacker color
                if isinstance(piece, str) and piece[0] == attacker_color and piece[1] == 'N':
                    return True
                
        # --- 2. Check for King Attacks (one square away) ---
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_moves:
            pr, pc = r + dr, c + dc
            if 0 <= pr < 8 and 0 <= pc < 8:
                piece = self.board[pr][pc]
                # Check for King piece (K) of the correct attacker color
                if isinstance(piece, str) and piece[0] == attacker_color and piece[1] == 'K':
                    return True

        # --- 3. Check for Pawn Attacks ---
        # Pawns attack diagonally, and their direction depends on their color.
        direction = 1 if attacker_color == 'b' else -1 # Black attacks downward (+1), White attacks upward (-1)
        
        for dc in [-1, 1]: # Check both diagonals
            pr, pc = r + direction, c + dc
            if 0 <= pr < 8 and 0 <= pc < 8:
                piece = self.board[pr][pc]
                # Pawns might be strings ('wp') or tuples (('wp', True)). Check for 'p'.
                if piece != '# ':
                    piece_type = piece[1] if isinstance(piece, str) else piece[0][1]
                    piece_color = piece[0] if isinstance(piece, str) else piece[0][0]
                    
                    if piece_color == attacker_color and piece_type == 'p':
                        return True

        # --- 4. Check for Sliding Piece Attacks (Rook, Bishop, Queen) ---
        # This reuses the logic from our earlier _get_slider_moves, but checks for the piece type.
        all_directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in all_directions:
            pr, pc = r + dr, c + dc
            
            while 0 <= pr < 8 and 0 <= pc < 8:
                piece = self.board[pr][pc]
                
                if piece == '# ':
                    pr += dr
                    pc += dc
                    continue # Keep sliding
                
                # Found a piece!
                piece_type = piece[1] if isinstance(piece, str) else piece[0][1]
                piece_color = piece[0] if isinstance(piece, str) else piece[0][0]

                if piece_color != attacker_color:
                    break # Blocked by friendly piece or captured piece
                
                # Check if the blocking piece is a valid attacker
                if (dr == 0 or dc == 0): # Horizontal/Vertical path (Rook/Queen)
                    if piece_type in ['R', 'Q']:
                        return True
                
                if (abs(dr) == abs(dc)): # Diagonal path (Bishop/Queen)
                    if piece_type in ['B', 'Q']:
                        return True
                        
                break # Blocked by a piece that is not the target attacker (e.g., a Knight)
                
        return False # If no attacking piece was found after all checks
    # In ChessEngine.py, inside the ChessEngine class:

    def _get_castling_moves(self, color):
        """Generates legal castling moves based on rights, path, and safety."""
        castling_moves = []
        
        # Determine rows and castling rights keys based on color
        king_row = 7 if color == 'w' else 0
        opponent_color = 'b' if color == 'w' else 'w'
        
        # King's starting position is always (king_row, 4)
        king_start = (king_row, 4)

        # A. Check if the King is currently in check
        if self.is_square_attacked(king_row, 4, opponent_color):
            return [] # Cannot castle while in check

        # --- King-side Castling (Short Castling) ---
        if self.castling_rights[color + 'K']:
            # 1. Path must be clear: f-file (col 5) and g-file (col 6)
            if self.board[king_row][5] == '# ' and self.board[king_row][6] == '# ':
                # 2. Squares crossed and landed on must not be attacked
                if (not self.is_square_attacked(king_row, 5, opponent_color) and # f-square
                    not self.is_square_attacked(king_row, 6, opponent_color)):    # g-square (landing)
                    
                    # Legal Castling: Move King from e to g
                    castling_moves.append((king_start, (king_row, 6)))

        # --- Queen-side Castling (Long Castling) ---
        if self.castling_rights[color + 'Q']:
            # 1. Path must be clear: b-file (col 1), c-file (col 2), and d-file (col 3)
            if (self.board[king_row][1] == '# ' and self.board[king_row][2] == '# ' and
                self.board[king_row][3] == '# '):
                # 2. Squares crossed and landed on must not be attacked
                if (not self.is_square_attacked(king_row, 3, opponent_color) and # d-square (crossing)
                    not self.is_square_attacked(king_row, 2, opponent_color)):    # c-square (landing)
                    
                    # Legal Castling: Move King from e to c
                    castling_moves.append((king_start, (king_row, 2)))
                    
        return castling_moves
    def _get_slider_moves(self, r, c, color, directions):
        """Generates moves for a piece that slides (Rook, Bishop, Queen)."""
        moves = []
        
        # Iterate through each direction (e.g., (1, 1) for southeast)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Keep sliding as long as we are on the board
            while 0 <= nr < 8 and 0 <= nc < 8:
                target_piece = self.board[nr][nc]
                
                # 1. Empty square: Valid move, keep sliding
                if target_piece == '# ':
                    moves.append((nr, nc))
                
                # 2. Opponent piece: Valid capture, STOP sliding
                elif target_piece[0] != color:
                    moves.append((nr, nc))
                    break 
                
                # 3. Own piece: Invalid move, STOP sliding (blocked)
                else:
                    break
                    
                nr += dr
                nc += dc
                
        return moves
    def moves_to_algebraic(self,move_dict):
        """
        Convert a dictionary of moves from (row, col) tuples to algebraic notation.
        
        Input:
            move_dict: {(start_row, start_col): [(end_row, end_col), ...], ...}
        
        Output:
            new_dict: {'e2': ['e3','e4'], ...}
        """
        def to_algebraic(row, col):
            return chr(col + ord('a')) + str(8 - row)

        new_dict = {}
        for start, ends in move_dict.items():
            start_alg = to_algebraic(*start)  # unpack tuple into row, col
            end_algs = [to_algebraic(*end) for end in ends]
            new_dict[start_alg] = end_algs

        return new_dict
    def _is_pawn_double_push(self, start, end, piece_type):
        """Checks if the move is a two-square pawn advance."""
        if piece_type != 'p':
            return False
        # Check if the move covers exactly two ranks
        return abs(start[0] - end[0]) == 2
    # In ChessEngine.py, inside the ChessEngine class:

    # In ChessEngine.py, inside the ChessEngine class:

    def _get_pseudo_legal_moves(self, color):
        """
        Generates all pseudo-legal moves for a given color, ignoring King safety.
        NOTE: Includes basic piece moves, pawn moves (not E.P. or Promotion), and Castling.
        Returns a dictionary: {(start_r, start_c): [(end_r, end_c), ...]}
        """
        moves = {}
        
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]

                if piece == '# ':
                    continue

                if isinstance(piece, tuple):
                    piece_symbol = piece[0]
                else:
                    piece_symbol = piece

                if piece_symbol[0] != color:
                    continue

                piece_type = piece_symbol[1]
                piece_moves = []

                # --- Pawn moves ---
                if piece_type == 'p':
                    direction = -1 if color == 'w' else 1
                    start_row = 6 if color == 'w' else 1

                    # Forward 1
                    nr = r + direction
                    if 0 <= nr < 8 and self.board[nr][c] == '# ':
                        piece_moves.append((nr, c))
                        # Forward 2 from start row
                        if r == start_row and self.board[r + 2 * direction][c] == '# ':
                            piece_moves.append((r + 2 * direction, c))

                    # Diagonal captures (including *potential* E.P. target)
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 8 and 0 <= nr < 8:
                            target_piece = self.board[nr][nc]
                            # Standard capture
                            if target_piece != '# ' and target_piece[0] != color:
                                piece_moves.append((nr, nc))
                            
                            # En Passant Generation (HIGH PRIORITY TODO: Integrate E.P. logic here)
                            if self.en_passant_target == (nr, nc):
                                # This is the generation of the E.P. move itself
                                piece_moves.append((nr, nc))
                                
                # --- Rook, Bishop, Queen (Slider moves) ---
                elif piece_type in ['R', 'B', 'Q']:
                    if piece_type == 'R':
                        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    elif piece_type == 'B':
                        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                    elif piece_type == 'Q':
                        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                    piece_moves = self._get_slider_moves(r, c, color, directions)

                # --- Knight moves ---
                elif piece_type == 'N':
                    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                                    (1, -2), (1, 2), (2, -1), (2, 1)]
                    for dr, dc in knight_moves:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            target_piece = self.board[nr][nc]
                            if target_piece == '# ' or target_piece[0] != color:
                                piece_moves.append((nr, nc))

                # --- King moves (Regular) ---
                elif piece_type == 'K':
                    king_directions = [(-1, -1), (-1, 0), (-1, 1),
                                    (0, -1), (0, 1),
                                    (1, -1), (1, 0), (1, 1)]
                    for dr, dc in king_directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            target_piece = self.board[nr][nc]
                            if target_piece == '# ' or target_piece[0] != color:
                                piece_moves.append((nr, nc))
                
                if piece_moves:
                    moves[(r, c)] = piece_moves

        # --- FINAL STEP: Add Castling Moves ---
        castling_moves_list = self._get_castling_moves(color)
        
        if castling_moves_list:
            king_start_pos = (7 if color == 'w' else 0, 4)
            
            if king_start_pos not in moves:
                moves[king_start_pos] = []
                
            for start, end in castling_moves_list:
                moves[king_start_pos].append(end)

        return moves
    # In ChessEngine.py, inside the ChessEngine class:

    def generate_all_legal_moves(self, color):
        """
        Generates ALL truly LEGAL moves for a given color.
        This filters pseudo-legal moves by checking if the King is left in check.
        """
        # 1. Generate all pseudo-legal moves
        pseudo_moves = self._get_pseudo_legal_moves(color)
        
        legal_moves = {}
        
        # 2. Filter every pseudo-legal move
        for start, end_list in pseudo_moves.items():
            r_start, c_start = start
            
            for end in end_list:
                r_end, c_end = end
                
                # Apply Move
                state_backup = self.apply_move(start, end)
                
                # Check for Legality: If the king is NOT in check after the move, it's legal
                if not self.is_in_check(color):
                    # Move is safe, add it to the final legal list
                    if start not in legal_moves:
                        legal_moves[start] = []
                    legal_moves[start].append(end)
                
                # Undo Move (CRITICAL: Must restore the board!)
                self.undo_move(start, end, state_backup)
                
        return legal_moves
