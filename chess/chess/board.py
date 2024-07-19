class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        # Initialize the board with pieces
        specialrow = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        pawns = ['p' for _ in range(8)]
        print(pawns)
        board = [['# ' for _ in range(8)] for _ in range(8)]
        # ^ create board, now we can modify with board[] statements 
        board[0] = ['w' + x for x in specialrow] # we can set our bottom and top rows to have special rows
        board[1] = ['w' + j for j in pawns]
        board[7] = ['b' + i for i in specialrow] ## iteration
        board[6] = ['b' + n for n in pawns]
        return board
    def print_board(self):
        for row in self.board:
            print(' '.join(row)) # Board is a list of 8 sublists with each list containing 1 row.
    
    
    
        