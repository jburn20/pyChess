from board import Board


def main():
    gameOn = True
    while gameOn:
        myboard = Board()
        myboard.print_board()
        
        player1 = input("Enter the x and y: ")

        
if __name__ == "__main__":
    main()