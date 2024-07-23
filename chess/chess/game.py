from board import Board


def main():
    gameOn = True
    while gameOn:
        myboard = Board()
        myboard.print_board()
        player1 = myboard.get_move() # a tuple formatted like ((x1,y1)(x2,y2)) then splits into start and end values
        print(player1[0],player1[1]) #player1[0] is the first input coord, e.g 'e2', player[1] is the second input coord, e.g 'e4'
        myboard.is_valid(player1[0],player1[1]) 
if __name__ == "__main__":
    main()