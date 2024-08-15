board = [['# ' for _ in range(8)] for _ in range(9)] #first range - len of individual list | second range - num# of lists
# ^ create board, now we can modify with board[] statements 
# Initialize the board with pieces
navcol = ['a','b','c','d','e','f','g','h']
navrow = [1,2,3,4,5,6,7,8]
board[8] = [" " + n for n in navcol]
specialrow = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
pawns = ['p' for _ in range(8)]
board[0] = ['w' + x for x in specialrow] # we can set our bottom and top rows to have special rows
board[1] = ['w' + j for j in pawns]
board[7] = ['b' + i for i in specialrow] ## iteration
board[6] = ['b' + n for n in pawns]
for i in navrow:
    print(i)
    board[i-1].append(str(8-i+1))
    



def print_board(board):
        for row in board:
            print(' '.join(row))
print_board(board)