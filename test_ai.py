import random
import math

EMPTY, X, O = " ", "X", "O"
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


def minimax(board, depth, maximizing, alpha, beta, stats):
    stats["positions"] += 1
    result = winner(board)
    if result == O:
        return 100 + depth
    if result == X:
        return -100 - depth
    if EMPTY not in board:
        return 0
    if depth == 0:
        return 0

    if maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = O
                best = max(best, minimax(board, depth - 1, False, alpha, beta, stats))
                board[i] = EMPTY
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    best = math.inf
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = X
            best = min(best, minimax(board, depth - 1, True, alpha, beta, stats))
            board[i] = EMPTY
            beta = min(beta, best)
            if beta <= alpha:
                break
    return best


def ai_move(board):
    stats = {"positions": 0}
    best_score = -math.inf
    moves = []
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = O
            score = minimax(board, 8, False, -math.inf, math.inf, stats)
            board[i] = EMPTY
            if score > best_score:
                best_score, moves = score, [i]
            elif score == best_score:
                moves.append(i)
    return random.choice(moves), stats["positions"]


def play_game(ai_first):
    board = [EMPTY] * 9
    ai_turn = ai_first
    while True:
        if ai_turn:
            move, _ = ai_move(board)
            board[move] = O
        else:
            available = [i for i, cell in enumerate(board) if cell == EMPTY]
            board[random.choice(available)] = X
        result = winner(board)
        if result:
            return "AI win" if result == O else "Random win"
        if EMPTY not in board:
            return "Draw"
        ai_turn = not ai_turn


def main():
    random.seed(42)
    results = {"AI win": 0, "Random win": 0, "Draw": 0}
    print("UNBEATABLE TIC-TAC-TOE AI — 10-GAME TEST")
    print("AI: Minimax + Alpha-Beta Pruning | Opponent: Random\n")
    for game in range(1, 11):
        result = play_game(ai_first=(game % 2 == 1))
        results[result] += 1
        print(f"Game {game:2}: {result}")
    print("\n--- FINAL RESULTS ---")
    print(f"AI wins:     {results['AI win']}")
    print(f"Random wins: {results['Random win']}")
    print(f"Draws:       {results['Draw']}")
    print("\nPASS: AI did not lose any game." if results["Random win"] == 0 else "FAIL: AI lost at least one game.")


if __name__ == "__main__":
    main()
