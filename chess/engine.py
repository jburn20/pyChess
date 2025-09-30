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
    
    def internal_board(self):
        """Return 8x8 logical board ignoring labels for calculations."""
        return [row[:8] for row in self.board[:8]]
# Add this helper function to the ChessEngine class:
    # In ChessEngine.py, inside the ChessEngine class:

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

    def generate_all_legal_moves(self, color, debug=False):
        """
        Generates all pseudo-legal moves for a given color, including castling.
        NOTE: This is still pseudo-legal; it does not filter moves that leave the King in check.
        Returns a dictionary: keys are starting positions (row, col),
        values are lists of valid ending positions [(row, col), ...].
        """
        moves = {}
        
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]

                # Skip empty squares
                if piece == '# ':
                    continue

                # Handle pawns as tuple (piece, has_moved)
                if isinstance(piece, tuple):
                    piece_symbol, has_moved = piece
                else:
                    piece_symbol = piece
                    # has_moved is implicitly tracked via r == start_row below

                # Only consider pieces of the given color
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

                    # Diagonal captures
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 8 and 0 <= nr < 8:
                            target_piece = self.board[nr][nc]
                            # Check for En Passant in a later step!
                            if target_piece != '# ' and target_piece[0] != color:
                                piece_moves.append((nr, nc))

                # --- Rook, Bishop, Queen (Slider moves using helper) ---
                elif piece_type == 'R':
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    piece_moves = self._get_slider_moves(r, c, color, directions)
                
                elif piece_type == 'B':
                    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                    piece_moves = self._get_slider_moves(r, c, color, directions)
                
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

                # --- King moves (Regular and Castling) ---
                elif piece_type == 'K':
                    # 1. Regular King moves (one step)
                    king_directions = [(-1, -1), (-1, 0), (-1, 1),
                                    (0, -1),          (0, 1),
                                    (1, -1),  (1, 0),  (1, 1)]
                    for dr, dc in king_directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            target_piece = self.board[nr][nc]
                            if target_piece == '# ' or target_piece[0] != color:
                                piece_moves.append((nr, nc))
                    
                    # 2. Add Castling Moves (Generated separately)
                    # _get_castling_moves returns [(start, end), ...] for the King's move
                    # We handle the integration of castling moves AFTER the main loop 
                    # to avoid duplicating logic inside every King square check.
                
                if piece_moves:
                    moves[(r, c)] = piece_moves
                    if debug:
                        print(f"Piece {piece} at {(r,c)} can move to: {piece_moves}")

        # --- FINAL STEP: Add Castling Moves to the King's list (Only one King exists) ---
        castling_moves_list = self._get_castling_moves(color)
        
        # We assume the King's starting position (r, c) is the same for all castling moves
        if castling_moves_list:
            # Find the King's start position: (7, 4) for White, (0, 4) for Black
            king_start_pos = (7 if color == 'w' else 0, 4)
            
            if king_start_pos not in moves:
                moves[king_start_pos] = []
                
            for start, end in castling_moves_list:
                # Add the King's destination (c1 or g1) to its list of moves
                moves[king_start_pos].append(end)

        return moves