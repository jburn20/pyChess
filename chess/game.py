from board import Board


def main():
    myboard = Board()
    gameOn = True
    myboard.print_board()
    turns = 0
    whiteTurn = True
    while gameOn:
        player = myboard.get_move() # a tuple formatted like ((x1,y1)(x2,y2)) then splits into start and end values
        # print(player[0],player[1]) #player[0] is the first input coord, ee2.g 'e2', player[1] is the second input coord, e.g 'e4'
        islegal , piece , attack = myboard.is_valid(player[0],player[1],whiteTurn)
        # print(islegal,piece,attack)
        print(f"Can white move? {whiteTurn}")
        print(f"Turns: {turns}")
        if islegal:
            myboard.make_move(player[0],player[1],piece)
            myboard.print_board()
            whiteTurn = myboard.switch_turn(whiteTurn)
            turns+=1
            print(f"Can white move? {whiteTurn}")
            print(f"Turns: {turns}")
            print(f"Attack:{attack}")
        else:
            print("Illegal Move")

        
        

if __name__ == "__main__":
    while True:
        try:
            main()
        except ValueError:
            print("Please enter valid start and end coordinates. Example: h7 h5")