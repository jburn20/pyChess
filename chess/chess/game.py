from board import Board


def main():
    gameOn = True
    while gameOn:
        myboard = Board()
        myboard.print_board()
        player = myboard.get_move() # a tuple formatted like ((x1,y1)(x2,y2)) then splits into start and end values
        print(player[0],player[1]) #player[0] is the first input coord, e.g 'e2', player[1] is the second input coord, e.g 'e4'
        islegal,piece = myboard.is_valid(player[0],player[1])
        if islegal == True:
            myboard.make_move(player[0],player[1])
        print(islegal,piece)
        

if __name__ == "__main__":
    main()