import random

board_size = int(input("Input a number as your board height and width: "))
symbol = None

## create_board() creates an empty board of board_size height and width
def create_board():
    board = []
    for x in range(0, board_size):
        column = []
        for y in range(0, board_size):
            column.append(None)
        board.append(column)
    return board

def display(board):
    rows = []
    for y in range(0, board_size):
        row = []
        for x in range(0, board_size):
            row.append(board[x][y])
        rows.append(row)

    row_num = 0
    for row in rows:
        output = ' '
        for square in row:
            if square is None:
                output += '_'
            else:
                output += square
        print  (' '.join(output))
        row_num += 1

board = create_board()

## player_symbol() assigns either X or O to the human player
def player_symbol():
    symbol = str(input ("Choose your symbol (X or O): "))
    while symbol != 'X' and symbol != 'O':
        symbol = str(input ("Please input a valid symbol (X or O): "))
    return symbol

## make_move(player, board, move_coords) checks if a space is empty and
##   replaces the space with the current player's symbol if so.
def make_move(player, board, move_coords):
    while True:
        if ((0 <= move_coords[0] < board_size
             and 0 <= move_coords[1] < board_size)
            and (board[move_coords[0]][move_coords[1]] == None)):
            board[move_coords[0]][move_coords[1]] = player
            break
        else:
            print("Please enter a valid move: ")
            move_ycoord = int(input("Enter your move's row number: "))
            move_xcoord = int(input("Enter your move's column number: "))
            move_coords = (move_xcoord, move_ycoord)

## player_move(board, player) prompts the human user to enter a move and
##   returns the move coordinates
def player_move(board, player):
    move_ycoord = int(input("Enter your move's row number: "))
    move_xcoord = int(input("Enter your move's column number: "))
    return (move_xcoord, move_ycoord)

## get_columns(board) creates a new board with the elements being the
##   columns of the original board
def get_columns(board):
    board_columns = []
    for x in range(0, board_size):
        column = [item[x] for item in board]
        board_columns.append(column)
    return board_columns

## get_diagonals(board) creates a list of all diagonals that are
##   board_size length from the original board
def get_diagonals(board):
    board_diagonals = []
    board_diagonals.append([board[x][x] for x in range(board_size)])
    board_diagonals.append([board[x][board_size-x-1] for x in range(board_size)])
    return board_diagonals

## get_winner(board) determines if any rows, columns, or diagonals are
##   composed of only Xs or Os, and returns the respective symbol if so
##   or None if there is no winner.
def get_winner(board):
    board_diagonals = get_diagonals(board)
    board_columns = get_columns(board)
    entire_board = board + board_columns + board_diagonals
    for x in range(0, len(entire_board)):
        if all(sym == 'X' for sym in entire_board[x]):
            return 'X'
        elif all(sym == 'O' for sym in entire_board[x]):
            return 'O'
    return None

## full_board(board) checks if there are any empty spaces in the board
##   and returns False if so and true otherwise
def full_board(board):
    for rows in board:
        for symbol in rows:
            if symbol == None:
                return False
    return True

## get_valid_moves(board) creates an array of all the coordinates that 
##   are None in the board.
def get_valid_moves(board):
    valid_moves = []
    for x, row in enumerate(board):
        for y, sym in enumerate(row):
            if sym == None:
                valid_moves.append((x, y))
    return valid_moves

## copy_board(board) creates a duplicate of the original board
def copy_board(board):
    new_board = create_board()
    for x in range(board_size):
        for y in range(board_size):
            new_board[x][y] = board[x][y]
    return new_board

## get_move(board, current_player, algorithm) returns a move coordinate
##   dependent on if the current_player is a human or the ai.
def get_move(board, current_player, algorithm):
    if algorithm == 'human':
        return player_move(board, current_player)
    else:
        return ai(board, current_player)

## get_opponent(current_player) returns the opposite symbol of the
##   current player.
def get_opponent(current_player):
    if current_player == 'X':
        return 'O'
    else:
        return 'X'

## minimax_score(board, current_player, minimax_player) calculates
##   every final resulting scores of a game given that each player
##   performs optimal moves by minimizing or maximizing their scores,
##   and returns either the maximum score or the minimum score
##   depending if the player can win or not.
def minimax_score(board, current_player, minimax_player):
    if get_winner(board) == minimax_player:
        return +1
    elif get_winner(board) != None:
        return -1
    elif full_board(board):
        return 0

    scores = []
    for move in get_valid_moves(board):
        new_board = copy_board(board)
        make_move(current_player, new_board, move)
        opponent = get_opponent(current_player)
        score = minimax_score(new_board, opponent, minimax_player)
        scores.append(score)
    if current_player == minimax_player:
        return max(scores)
    else:
        return min(scores)

## ai(board, current_player) returns the most optimal move coordinates
##    based on the highest possible score and odds of winning
def ai(board, current_player):
    best_move = None
    best_score = None
    for move in get_valid_moves(board):
        new_board = copy_board(board)
        make_move(current_player, new_board, move)
        opponent = get_opponent(current_player)
        score = minimax_score(new_board, opponent, current_player)
        if best_score == None or score > best_score:
            best_move = move
            best_score = score
    return best_move

## main() initializes the tic-tac-toe game against an AI
def main():
    player = player_symbol()
    if player == 'X':
        players = [('X', 'human'), ('O', 'minimax')]
    else:
        players = [('X', 'minimax'), ('O', 'human')]
    turn = 0
    current_player = None
    while True:
        if turn % 2 == 0:
            current_player = 'X'
            algorithm = players[0][1]
        else:
            current_player = 'O'
            algorithm = players[1][1]
        display(board)
        move_coords = get_move(board, current_player, algorithm)
        make_move(current_player, board, move_coords)
        turn += 1
        if get_winner(board) != None:
            display(board)
            print(get_winner(board) + " wins!")
            break
        if full_board(board):
            display(board)
            print("Tie game!")
            break
main()
