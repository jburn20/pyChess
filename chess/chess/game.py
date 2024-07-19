from board import Board


def main():
    gameOn = True
    while gameOn:
        myboard = Board()
        current = myboard.print_board()
        player1 = input("Enter the x and y: ")
        print(current)
        
        
if __name__ == "__main__":
    main()