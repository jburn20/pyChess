class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        # Initialize the board with pieces
        specialrow = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        board = [['#' for _ in range(8)] for _ in range(8)]
        # ^ create board, now we can modify with board[] statements 
        board[0] = ['w' + x for x in specialrow] # we can set our bottom and top rows to have special rows
        board[7] = ['b' + i for i in specialrow] ## iteration
        return board
    def print_board(self):
        for row in self.board:
            print(' '.join(row))
    def read_board(self):
        for row in self.board:
            return row
    def tester(self):
        print()
    def getPiePos(board, positionlist:str):
        print(type(posses))
        posses = positionlist.split(",")
        return board[posses[0]][posses[1]]
    
        