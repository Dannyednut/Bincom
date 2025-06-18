import random

def print_board(board):
    """Prints the current state of the board."""
    print("-------------")
    for i in range(3):
        print("|", board[i][0], "|", board[i][1], "|", board[i][2], "|")
        print("-------------")

def check_win(board, player):
    """Checks if the given player has won."""
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == player:
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False

def check_tie(board):
    """Checks if the game is a tie."""
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False  # There's still an empty space
    return True

def player_move(board, player):
    """Gets the player's move and updates the board."""
    while True:
        try:
            row = int(input(f"Player {player}, enter the row (0-2): "))
            col = int(input(f"Player {player}, enter the column (0-2): "))

            if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == " ":
                board[row][col] = player
                return
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter numbers between 0 and 2.")

def computer_move_random(board, computer_player):
    """Computer makes a random valid move."""
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == " ":
            board[row][col] = computer_player
            print(f"Computer placed {computer_player} at row {row}, column {col}")
            return

def computer_move_intelligent(board, computer_player, human_player):
    """Computer tries to win or block the player.  If all else fails, random move."""

    # 1. Check for winning move for the computer
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = computer_player
                if check_win(board, computer_player):
                    print(f"Computer placed {computer_player} at row {i}, column {j} to win!")
                    return
                board[i][j] = " "  # Undo the move

    # 2. Check for blocking move for the human
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = human_player
                if check_win(board, human_player):
                    board[i][j] = computer_player
                    print(f"Computer placed {computer_player} at row {i}, column {j} to block you!")
                    return
                board[i][j] = " "  # Undo the move

    # 3. If no winning or blocking move, make a random move
    computer_move_random(board, computer_player)  # Call the random move function


def play_game(computer_opponent = "random"): # Default to a random computer opponent
    """Plays the Tic-Tac-Toe game."""
    board = [[" " for _ in range(3)] for _ in range(3)]  # Creates a 3x3 board
    player = "X"  # First player is X
    computer_player = "O"

    if computer_opponent not in ["random", "intelligent", "none"]:
        print("Invalid computer opponent choice.  Using random.")
        computer_opponent = "random"

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        if player == "X":
            player_move(board, player)
        else:
            if computer_opponent == "random":
                computer_move_random(board, computer_player)
            elif computer_opponent == "intelligent":
                computer_move_intelligent(board, computer_player, "X")  # X is the human player
            else: #computer_opponent == "none":  Player O's turn (second human player)
                player_move(board, player) #Let the second player move
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} wins!")
            break
        if check_win(board, computer_player):
            print(f"Player {computer_player} wins!") #Or the computer
            break


        if check_tie(board):
            print("It's a tie!")
            break

        player = "O" if player == "X" else "X"  # Switch players

# Example usage:
if __name__ == "__main__":
    while True:
        mode = input("Play against (random/intelligent/none) computer or two-player (type 'random', 'intelligent', or 'none'): ").lower()
        if mode in ["random", "intelligent", "none"]:
            play_game(mode)
            break
        else:
            print("Invalid mode selected. Please type 'random', 'intelligent', or 'none'.")


    another_game = input("Play another game? (yes/no): ").lower()
    while another_game == "yes":
        while True:
            mode = input("Play against (random/intelligent/none) computer or two-player (type 'random', 'intelligent', or 'none'): ").lower()
            if mode in ["random", "intelligent", "none"]:
                play_game(mode)
                break
            else:
                print("Invalid mode selected. Please type 'random', 'intelligent', or 'none'.")
        another_game = input("Play another game? (yes/no): ").lower()
    print("Thanks for playing!")