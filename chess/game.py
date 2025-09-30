from board import Board
from engine import ChessEngine

def main():
    myboard = Board()
    myengine = ChessEngine()
    
    gameOn = True
    whiteTurn = True
    turns = 0
    
    myboard.print_board()

    while gameOn:
        current_color = 'w' if whiteTurn else 'b'
        
        # 1. Sync the Engine with the current Board state
        myengine.sync_board(myboard) 
        
        # 2. Generate ALL truly legal moves (includes the King safety filter)
        legal_moves = myengine.generate_all_legal_moves(current_color)
        
        # --- Checkmate/Stalemate Placeholder ---
        # NOTE: This will be refined when we detect Check status properly
        if not legal_moves:
            print(f"Game Over. {current_color.upper()} has no legal moves.")
            # Checkmate or Stalemate logic goes here (after we implement is_in_check properly)
            gameOn = False
            continue

        print(f"\n--- {current_color.upper()}'s Turn ({'White' if whiteTurn else 'Black'}) ---")
        print(f"Turns: {turns}")
        
        try:
            # 3. Get raw input string (e.g., 'e2 e4' or 'moves')
            # Assuming you created this helper in Board.py
            raw_input = myboard.get_raw_input() 
            
            # --- COMMAND CHECK: List Available Moves ---
            if raw_input.lower() in ['moves', 'move']:
                print("\n--- AVAILABLE LEGAL MOVES ---")
                
                # Format and print the generated legal_moves dictionary
                for start_coord, end_list in legal_moves.items():
                    # Convert internal (6, 4) back to algebraic 'e2'
                    start_alg = myboard.coord_to_alg(start_coord) 
                    
                    # Convert the list of ends to algebraic
                    end_alg_list = [myboard.coord_to_alg(end_coord) for end_coord in end_list]
                    
                    print(f"• {start_alg} -> {', '.join(end_alg_list)}")
                continue # Skip the rest of the loop and prompt for input again

            # 4. Process Move Input (e.g., 'e2 e4')
            start_alg, end_alg = raw_input.split()
            
            # Convert algebraic to internal coordinates
            start_coord = myboard.alg_to_coord(start_alg)
            end_coord = myboard.alg_to_coord(end_alg)
            
            # 5. Get piece to move (needed for make_move)
            piece_to_move = myboard.board[start_coord[0]][start_coord[1]]
            
            # 6. VALIDATION VIA LOOKUP (Relies entirely on the generated legal_moves)
            is_valid_start = start_coord in legal_moves
            
            if not is_valid_start:
                print(f"Illegal Move: No piece at {start_alg} or that piece has no moves.")
                continue

            is_valid_end = end_coord in legal_moves[start_coord]
            
            if is_valid_end:
                # 7. Execute the move
                myboard.make_move(start_coord, end_coord, piece_to_move)
                myboard.print_board()
                
                # Update game state
                whiteTurn = myboard.switch_turn(whiteTurn)
                turns += 1
                
            else:
                print("Illegal Move: Target square is not a valid destination for that piece.")
                
        except (ValueError, IndexError):
            # Catches errors from split/conversion or invalid coordinates
            print("Invalid input. Please enter valid algebraic coordinates (e.g., h7 h5) or 'moves'.")
            
        except Exception as e:
            # General catch-all for development
            print(f"An unexpected error occurred: {e}")
            
# The __name__ == "__main__" block is fine as is
if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            # This outer try/except block is for unexpected program crashes
            print(f"Game crashed unexpectedly: {e}")
            break