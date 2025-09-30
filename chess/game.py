from board import Board
from engine import ChessEngine # Assuming you renamed ChessEngine.py to engine.py

def main():
    myboard = Board()
    myengine = ChessEngine()  # 1. Instantiate the Engine
    
    gameOn = True
    whiteTurn = True
    turns = 0
    
    myboard.print_board()

    while gameOn:
        current_color = 'w' if whiteTurn else 'b'
        
        # 2. Sync the Engine's internal board with the current game board
        myengine.sync_board(myboard)
        
        # 3. Generate ALL legal moves for the current player
        # This is a dictionary: {(start_r, start_c): [(end_r, end_c), ...]}
        legal_moves = myengine.generate_all_legal_moves(current_color)
        
        # Check for Checkmate/Stalemate (We'll implement this later)
        if not legal_moves:
            # This will be refined when we implement check logic
            print(f"Game Over. {current_color} has no legal moves.")
            gameOn = False
            continue

        print(f"\n--- {current_color.upper()}'s Turn ({'White' if whiteTurn else 'Black'}) ---")
        print(f"Turns: {turns}")
        
        try:
            # 4. Get the player's move (returns (r1, c1), (r2, c2))
            start_coord, end_coord = myboard.get_move()
            
            # 5. Get the piece from the board to pass to make_move
            piece_to_move = myboard.board[start_coord[0]][start_coord[1]]
            
            # --- VALIDATION VIA LOOKUP ---
            is_valid_start = start_coord in legal_moves
            
            if not is_valid_start:
                print(f"Illegal Move: No piece at {start_coord} or that piece has no moves.")
                continue

            is_valid_end = end_coord in legal_moves[start_coord]
            
            if is_valid_end:
                # 6. Execute the move! (Note: We need to update make_move later to handle state)
                myboard.make_move(start_coord, end_coord, piece_to_move)
                myboard.print_board()
                
                # Update game state
                whiteTurn = myboard.switch_turn(whiteTurn)
                turns += 1
                
            else:
                print("Illegal Move: Target square is not a valid destination for that piece.")
                
        except ValueError:
            # Catches errors from split/conversion inside get_move/main
            print("Please enter valid start and end coordinates. Example: h7 h5")
        
        except IndexError:
            # Catches if the board index is out of bounds (user input error)
            print("Invalid board coordinate entered.")
    
        except Exception as e:
            # General catch-all for development
            print(f"An unexpected error occurred: {e}")
            
# The __name__ == "__main__" block is fine as is
if __name__ == "__main__":
    while True:
        try:
            main()
        except ValueError:
            print("Please enter valid start and end coordinates. Example: h7 h5")