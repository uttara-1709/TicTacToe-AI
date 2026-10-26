import tkinter as tk
from tkinter import messagebox
import random
import math

EMPTY = " "
HUMAN = "X"
AI = "O"
WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def terminal_score(board, depth):
    result = winner(board)
    if result == AI:
        return 100 + depth
    if result == HUMAN:
        return -100 - depth
    if EMPTY not in board:
        return 0
    return None


def minimax(board, depth, maximizing, alpha, beta, stats):
    """Return the best score for AI (O), counting searched positions."""
    stats["positions"] += 1
    score = terminal_score(board, depth)
    if score is not None:
        return score
    if depth == 0:
        return 0

    if maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                best = max(best, minimax(board, depth - 1, False, alpha, beta, stats))
                board[i] = EMPTY
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best

    best = math.inf
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = HUMAN
            best = min(best, minimax(board, depth - 1, True, alpha, beta, stats))
            board[i] = EMPTY
            beta = min(beta, best)
            if beta <= alpha:
                break
    return best


def best_move(board, difficulty):
    available = [i for i, value in enumerate(board) if value == EMPTY]
    stats = {"positions": 0}
    if not available:
        return None, stats["positions"]

    if difficulty == "Easy":
        return random.choice(available), 0

    search_depth = 2 if difficulty == "Medium" else len(available)
    best_score = -math.inf
    choices = []
    for i in available:
        board[i] = AI
        score = minimax(board, search_depth - 1, False, -math.inf, math.inf, stats)
        board[i] = EMPTY
        if score > best_score:
            best_score = score
            choices = [i]
        elif score == best_score:
            choices.append(i)
    return random.choice(choices), stats["positions"]


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI | Minimax Lab")
        self.root.resizable(False, False)
        self.root.configure(bg="#f3f5f9")

        self.board = [EMPTY] * 9
        self.game_over = False
        self.ai_pending = False
        self.scores = {"Player": 0, "AI": 0, "Draws": 0}
        self.last_positions = 0
        self.difficulty = tk.StringVar(value="Hard")
        self.buttons = []

        tk.Label(root, text="TIC-TAC-TOE AI", font=("Arial", 22, "bold"),
                 bg="#f3f5f9", fg="#182238").grid(row=0, column=0, columnspan=3, pady=(16, 2))
        tk.Label(root, text="Minimax + Alpha-Beta Pruning", font=("Arial", 10),
                 bg="#f3f5f9", fg="#596579").grid(row=1, column=0, columnspan=3, pady=(0, 12))

        tk.Label(root, text="Difficulty:", font=("Arial", 11, "bold"), bg="#f3f5f9").grid(row=2, column=0, sticky="e", padx=6)
        menu = tk.OptionMenu(root, self.difficulty, "Easy", "Medium", "Hard", command=self.change_difficulty)
        menu.config(font=("Arial", 10), width=10, bg="white", relief="flat")
        menu.grid(row=2, column=1, sticky="w", pady=4)

        self.status = tk.Label(root, text="Your turn — you are X", font=("Arial", 12, "bold"),
                               bg="#f3f5f9", fg="#26344d")
        self.status.grid(row=3, column=0, columnspan=3, pady=8)

        for i in range(9):
            button = tk.Button(root, text="", font=("Arial", 25, "bold"), width=4, height=2,
                               bg="white", activebackground="#e7edf8", relief="flat", bd=0,
                               command=lambda index=i: self.human_move(index))
            button.grid(row=4 + i // 3, column=i % 3, padx=4, pady=4)
            self.buttons.append(button)

        self.stats_label = tk.Label(root, text="Player wins: 0   AI wins: 0   Draws: 0",
                                    font=("Arial", 10, "bold"), bg="#f3f5f9", fg="#26344d")
        self.stats_label.grid(row=7, column=0, columnspan=3, pady=(12, 3))
        self.analysis_label = tk.Label(root, text="AI positions evaluated: 0",
                                       font=("Arial", 9), bg="#f3f5f9", fg="#596579")
        self.analysis_label.grid(row=8, column=0, columnspan=3, pady=3)

        tk.Button(root, text="New Game", font=("Arial", 10, "bold"), width=12,
                  command=self.reset_game, bg="#dce6f7", relief="flat").grid(row=9, column=0, pady=14)
        tk.Button(root, text="Reset Scores", font=("Arial", 10), width=12,
                  command=self.reset_scores, bg="#e8ebf0", relief="flat").grid(row=9, column=1, pady=14)
        tk.Button(root, text="How It Works", font=("Arial", 10), width=12,
                  command=self.show_help, bg="#e8ebf0", relief="flat").grid(row=9, column=2, pady=14)

    def change_difficulty(self, _choice=None):
        if not self.game_over and self.board.count(EMPTY) == 9:
            self.status.config(text=f"{self.difficulty.get()} mode — your turn (X)")

    def human_move(self, index):
        if self.game_over or self.ai_pending or self.board[index] != EMPTY:
            return
        self.board[index] = HUMAN
        self.update_board()
        if self.check_game_end():
            return
        self.ai_pending = True
        self.status.config(text=f"{self.difficulty.get()} AI is thinking...")
        self.root.after(120, self.ai_move)

    def ai_move(self):
        self.ai_pending = False
        if self.game_over:
            return
        move, positions = best_move(self.board, self.difficulty.get())
        self.last_positions = positions
        self.analysis_label.config(text=f"AI positions evaluated: {positions:,}")
        if move is not None:
            self.board[move] = AI
        self.update_board()
        if not self.check_game_end():
            self.status.config(text="Your turn — you are X")

    def update_board(self):
        for i, button in enumerate(self.buttons):
            value = self.board[i]
            button.config(text="" if value == EMPTY else value,
                          state=tk.DISABLED if value != EMPTY or self.game_over else tk.NORMAL,
                          fg="#2463eb" if value == HUMAN else "#d14c4c")

    def check_game_end(self):
        result = winner(self.board)
        if result == HUMAN:
            self.scores["Player"] += 1
            message = "You win!"
        elif result == AI:
            self.scores["AI"] += 1
            message = "AI wins!"
        elif EMPTY not in self.board:
            self.scores["Draws"] += 1
            message = "It's a draw!"
        else:
            return False

        self.game_over = True
        self.status.config(text=message)
        self.update_board()
        self.update_scores()
        messagebox.showinfo("Game Over", message)
        return True

    def update_scores(self):
        self.stats_label.config(text=f"Player wins: {self.scores['Player']}   AI wins: {self.scores['AI']}   Draws: {self.scores['Draws']}")

    def reset_game(self):
        self.board = [EMPTY] * 9
        self.game_over = False
        self.ai_pending = False
        self.last_positions = 0
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL, fg="#2463eb")
        self.status.config(text="Your turn — you are X")
        self.analysis_label.config(text="AI positions evaluated: 0")

    def reset_scores(self):
        self.scores = {"Player": 0, "AI": 0, "Draws": 0}
        self.update_scores()

    def show_help(self):
        messagebox.showinfo(
            "How the AI works",
            "Easy: chooses a random empty cell.\n\n"
            "Medium: searches a limited number of moves.\n\n"
            "Hard: searches the remaining game tree using Minimax.\n\n"
            "Alpha-beta pruning skips branches that cannot improve the decision.\n"
            "In Hard mode, optimal play means the AI cannot be beaten."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
