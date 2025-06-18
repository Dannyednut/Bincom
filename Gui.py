import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.computer_mode = "none"  # Options: "none", "random", "intelligent"

        self.setup_menu()
        self.create_board()

    def setup_menu(self):
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value="none")
        tk.OptionMenu(mode_frame, self.mode_var, "none", "random", "intelligent").pack(side=tk.LEFT)
        tk.Button(mode_frame, text="Start Game", command=self.reset_game).pack(side=tk.LEFT)

    def create_board(self):
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text=" ", width=5, height=2,
                                font=("Arial", 24), command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_click(self, row, col):
        if self.board[row][col] == " " and self.current_player == "X":
            self.board[row][col] = "X"
            self.update_button(row, col, "X")
            if self.check_game_end("X"):
                return
            self.current_player = "O"
            self.root.after(500, self.computer_move)

    def computer_move(self):
        mode = self.mode_var.get()
        if mode == "random":
            self.computer_move_random()
        elif mode == "intelligent":
            self.computer_move_intelligent()
        self.current_player = "X"

    def computer_move_random(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        if empty:
            row, col = random.choice(empty)
            self.board[row][col] = "O"
            self.update_button(row, col, "O")
            self.check_game_end("O")

    def computer_move_intelligent(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    if self.check_win("O"):
                        self.update_button(i, j, "O")
                        self.check_game_end("O")
                        return
                    self.board[i][j] = " "

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "X"
                    if self.check_win("X"):
                        self.board[i][j] = "O"
                        self.update_button(i, j, "O")
                        self.check_game_end("O")
                        return
                    self.board[i][j] = " "

        self.computer_move_random()

    def update_button(self, row, col, symbol):
        self.buttons[row][col]["text"] = symbol
        self.buttons[row][col]["state"] = "disabled"

    def check_game_end(self, player):
        if self.check_win(player):
            messagebox.showinfo("Game Over", f"Player {player} wins!")
            self.disable_all_buttons()
            self.reset_game()
            return True
        elif self.check_tie():
            messagebox.showinfo("Game Over", "It's a tie!")
            return True
        return False

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
            if all(self.board[j][i] == player for j in range(3)):
                return True

        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True

        return False

    def check_tie(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn["state"] = "disabled"

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = " "
                self.buttons[i][j]["state"] = "normal"

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
