from flask import Flask, render_template, jsonify, request
from collections import deque

app = Flask(__name__)

# Winning combinations
WINNING_POSITIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]              # Diagonals
]

# Check if there's a winner
def check_winner(board):
    for positions in WINNING_POSITIONS:
        if board[positions[0]] == board[positions[1]] == board[positions[2]] and board[positions[0]] != ' ':
            return board[positions[0]]  # Return 'X' or 'O'
    return None

# Check if the board is full (draw)
def is_draw(board):
    return all(cell != ' ' for cell in board)

# AI to find the best move
def find_best_move(board, player):
    opponent = 'O' if player == 'X' else 'X'
    for i in range(9):
        if board[i] == ' ':
            board[i] = player
            if check_winner(board) == player:
                board[i] = ' '  # Undo move
                return i
            board[i] = ' '  # Undo move
    # Block opponent's winning move
    for i in range(9):
        if board[i] == ' ':
            board[i] = opponent
            if check_winner(board) == opponent:
                board[i] = ' '  # Undo move
                return i
            board[i] = ' '  # Undo move
    # Otherwise, take the first available spot
    for i in range(9):
        if board[i] == ' ':
            return i

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make-move', methods=['POST'])
def make_move():
    data = request.json
    board = data['board']
    current_player = data['player']

    if check_winner(board):
        return jsonify({'status': 'finished', 'winner': check_winner(board)})

    if is_draw(board):
        return jsonify({'status': 'finished', 'winner': 'Draw'})

    if current_player == 'O':  # AI's turn
        move = find_best_move(board, current_player)
        board[move] = 'O'
        winner = check_winner(board)
        if winner:
            return jsonify({'status': 'finished', 'winner': winner, 'board': board})
        if is_draw(board):
            return jsonify({'status': 'finished', 'winner': 'Draw', 'board': board})

    return jsonify({'status': 'ongoing', 'board': board})

if __name__ == '__main__':
    app.run(debug=True)
