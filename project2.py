import tkinter as tk
from tkinter import messagebox
import random
import copy

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.board = {i: str(i) for i in range(1, 10)}  # dictionary to manage board
        self.buttons = {}
        self.player_letter = tk.StringVar(value="X")
        self.computer_letter = ""
        self.current_player = ""
        self.mode = tk.StringVar(value="computer")
        self.start_choice = tk.StringVar(value="Yes")
        self.setup_initial_screen()

    def setup_initial_screen(self):
        """Set up the initial screen with role selection and disabled board."""
        tk.Label(self.window, text="Tic-Tac-Toe", font=("Arial", 16, "bold")).pack(pady=10)

        # main frame for role selection and board
        main_frame = tk.Frame(self.window)
        main_frame.pack(padx=20, pady=5)

        # play With section
        play_frame = tk.Frame(main_frame)
        play_frame.pack(anchor="w")
        tk.Label(play_frame, text="Play With", font=("Arial", 12)).pack(anchor="w")
        tk.Radiobutton(play_frame, text="Computer", variable=self.mode, value="computer", font=("Arial", 10)).pack(anchor="w")
        tk.Radiobutton(play_frame, text="Player 2", variable=self.mode, value="player", font=("Arial", 10)).pack(anchor="w")

        # Select letter section
        letter_frame = tk.Frame(main_frame)
        letter_frame.pack(anchor="w", pady=5)
        tk.Label(letter_frame, text="Select", font=("Arial", 12)).pack(anchor="w")
        tk.Radiobutton(letter_frame, text="X", variable=self.player_letter, value="X", font=("Arial", 10)).pack(anchor="w")
        tk.Radiobutton(letter_frame, text="O", variable=self.player_letter, value="O", font=("Arial", 10)).pack(anchor="w")

        # Start the game section
        start_frame = tk.Frame(main_frame)
        start_frame.pack(anchor="w", pady=5)
        tk.Label(start_frame, text="Start the game", font=("Arial", 12)).pack(anchor="w")
        tk.Radiobutton(start_frame, text="Yes", variable=self.start_choice, value="Yes", font=("Arial", 10)).pack(anchor="w")
        tk.Radiobutton(start_frame, text="No", variable=self.start_choice, value="No", font=("Arial", 10)).pack(anchor="w")

        # Start button
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=5)
        tk.Button(button_frame, text="start", command=self.start_game, font=("Arial", 10), relief="raised").pack(side="right")

        # Create the board (initially disabled)
        self.create_board(main_frame)

    def create_board(self, parent_frame):
        """Create the 3x3 game board with buttons, initially disabled."""
        board_frame = tk.Frame(parent_frame)
        board_frame.pack(pady=10)
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            btn = tk.Button(board_frame, text=self.board[i], font=("Arial", 20), width=5, height=2,
                            bg="#d3d3d3", relief="raised", bd=3,
                            command=lambda x=i: self.button_click(x))
            btn.grid(row=row, column=col, padx=2, pady=2)
            btn.config(state="disabled")  # Initially disable the buttons
            self.buttons[i] = btn

    def start_game(self):
        """Enable the board and start the game only if 'Yes' is selected."""
        if self.start_choice.get() == "Yes":
            # Enable all board buttons
            for btn in self.buttons.values():
                btn.config(state="normal")

            # Set up the game
            self.computer_letter = "O" if self.player_letter.get() == "X" else "X"
            self.current_player = "X"  # Since "Yes" means Player 1 starts

            # If computer mode and Player 2/Computer should start (not applicable since "No" prevents start)
            if self.mode.get() == "computer" and self.current_player == self.computer_letter:
                self.computer_move()
        else:
            messagebox.showinfo("Game Not Started", "Please select 'Yes' to start the game.")

    def button_click(self, pos):
        """Handle button clicks for player moves."""
        if self.board[pos] not in ["X", "O"]:
            self.board[pos] = self.current_player
            self.buttons[pos].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.end_game(f"{'Player 1' if self.current_player == self.player_letter.get() else 'Computer/Player 2'} wins!")
                return
            if self.is_full():
                self.end_game("It's a draw!")
                return
            self.current_player = "O" if self.current_player == "X" else "X"
            if self.mode.get() == "computer" and self.current_player == self.computer_letter:
                self.computer_move()
        else:
            messagebox.showerror("Invalid Move", "That spot is already taken!")

    def computer_move(self):
        """Implement computer's smart move strategy."""
        for pos in self.get_available_moves():
            board_copy = copy.deepcopy(self.board)
            board_copy[pos] = self.computer_letter
            if self.check_winner_dict(board_copy, self.computer_letter):
                self.make_move(pos)
                return

        for pos in self.get_available_moves():
            board_copy = copy.deepcopy(self.board)
            board_copy[pos] = self.player_letter.get()
            if self.check_winner_dict(board_copy, self.player_letter.get()):
                self.make_move(pos)
                return

        if self.board[5] == "5":
            self.make_move(5)
            return

        corners = [1, 3, 7, 9]
        random.shuffle(corners)
        for pos in corners:
            if self.board[pos] == str(pos):
                self.make_move(pos)
                return

        moves = self.get_available_moves()
        if moves:
            self.make_move(random.choice(moves))

    def make_move(self, pos):
        """Make a move and update the board."""
        self.board[pos] = self.current_player
        self.buttons[pos].config(text=self.current_player)
        if self.check_winner(self.current_player):
            self.end_game("Computer wins!")
            return
        if self.is_full():
            self.end_game("It's a draw!")
            return
        self.current_player = self.player_letter.get()

    def get_available_moves(self):
        """Return list of available positions."""
        return [i for i in range(1, 10) if self.board[i] not in ["X", "O"]]

    def check_winner(self, letter):
        """Check if the given letter has won."""
        return self.check_winner_dict(self.board, letter)

    def check_winner_dict(self, board, letter):
        """Check win conditions using dictionary board."""
        for i in [1, 4, 7]:
            if board[i] == board[i+1] == board[i+2] == letter:
                return True
        for i in [1, 2, 3]:
            if board[i] == board[i+3] == board[i+6] == letter:
                return True
        if board[1] == board[5] == board[9] == letter:
            return True
        if board[3] == board[5] == board[7] == letter:
            return True
        return False

    def is_full(self):
        """Check if the board is full."""
        return all(self.board[i] in ["X", "O"] for i in range(1, 10))

    def end_game(self, message):
        """Display game result and ask to play again."""
        # Disable the board again
        for btn in self.buttons.values():
            btn.config(state="disabled")
        messagebox.showinfo("Game Over", message)
        if messagebox.askyesno("Play Again", "Would you like to play another game?"):
            self.reset_game()
        else:
            self.window.destroy()

    def reset_game(self):
        """Reset the game for a new round."""
        self.board = {i: str(i) for i in range(1, 10)}
        for widget in self.window.winfo_children():
            widget.destroy()
        self.buttons = {}
        self.setup_initial_screen()

if __name__ == "__main__":
    game = TicTacToe()
    game.window.mainloop()