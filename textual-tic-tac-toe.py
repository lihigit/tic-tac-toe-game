#
# Lihi's Tic Tac Toe Python game!
#
# Author:       Lihi V
# Date:         October 2020
# Version:      1.0
# Description:  A Tic Tac Toe game, including 4 players' options:
#               human, AI: impossible, AI: medium and AI: easy.
#

from random import choice
import copy

# ============= Constants =============

# Players' constants
NUMBER_OF_PLAYERS = 2
DEFAULT_STARTING_PLAYER = 0
PLAYER_SYMBOLS = ['X', 'O']
PLAYER_TYPES = ['user', 'easy', 'medium', 'impossible']

# Board's constants
WIN_LEN = 3
BOARD_SIZE = 3
DIMENSIONS = 2

# Commands' constants
COMMANDS = ['start', 'exit']
COMMAND_LEN = 1

# Minimax values:
X_MINIMAX = 1
O_MINIMAX = -1

# Instructions for the user:
PLAYERS_MESSAGE = '''You can choose a match between any of the following:
        "user"          - that's you! and/or a friend
        "easy"          - an easy to beat AI
        "medium"        - a medium level AI
        "impossible"    - an impossible to beat AI'''
INSTRUCTIONS_MESSAGE = '''To start a match, type:
    start <player> <player>
    Examples: 
        start easy easy
        start user impossible
        
To exit, type:
    exit'''

# ============= Classes =============

# A Tic Tac Toe game board
class Board:
    board_size = BOARD_SIZE
    empty_cell = ' '

    def __init__(self):
        self.cells = []
        for i in range(self.board_size):
            self.cells.append([self.empty_cell] * self.board_size)

    # Board -> None
    # Displays a visual representation of the board's current state on the screen
    def print_board(self):
        print()
        # Print the columns coordinates:
        line = '  | '
        for i in range(self.board_size):
            line += f'{i} '
        print(line + '|')
        # Print the row coordinates and the rest of the Board
        self.print_board_border()
        for i in range(self.board_size):
            line = f'{i } |'
            for j in range(self.board_size):
                line += f' {self.cells[i][j]}'
            print(line + ' |')
        self.print_board_border()
        print()

    # Board -> None
    # Print the Board top and bottom borders
    def print_board_border(self):
        print("-" * (2 * self.board_size + 5))

    # Board, char, int, int -> None
    # Update the Board to include player_symbol at location [col, row]
    def update_col_row(self, player_symbol, col, row):
        col = int(col)
        row = int(row)
        self.cells[row % self.board_size][col % self.board_size] = player_symbol  # the modulo is to prevent access to an out of range index

    # Board, int, int -> char
    # Return the char at location [col, row] on the board
    def symbol_at_location(self, col, row):
        return self.cells[int(row) % 3][int(col) % 3]

    # Board -> boolean
    # Return True if the board is full and False otherwise
    def full(self):
        return self.empty_cells_indexes() == []

    # Board -> list of lists
    # Return a list of the empty cells on the board [col, row]
    def empty_cells_indexes(self):
        empty_cells = []
        for row in range(board.board_size):
            for col in range(board.board_size):
                if self.cells[row][col] == board.empty_cell:
                    empty_cells.append([col, row])
        return empty_cells

    # Board, int, int -> boolean
    # Return True if the location [col, row] on the board is empty
    # Return False otherwise
    def is_empty(self, col, row):
        col = int(col)
        row = int(row)
        return self.symbol_at_location(col, row) == self.empty_cell


# Turn: keeps track on who's the current player
class Turn:
    def __init__(self, first=0):
        self.turn = first

    # Turn -> int
    # Return the current player's index
    def get(self):
        return self.turn

    # Turn -> None
    # Change the turn to the next Player
    def change(self):
        self.turn = (self.turn + 1) % NUMBER_OF_PLAYERS


# Basic Player attributes and functions
class Player:
    # List of all the currently active Players objects
    players = []
    # The number of currently active Players
    n = 0

    def __new__(cls):
        # Check that there are exactly the defined number of players,
        # if so, proceed and create a new Player object.
        if len(cls.players) < NUMBER_OF_PLAYERS:
            return object.__new__(cls)

    def __init__(self):
        self.symbol = PLAYER_SYMBOLS[len(self.players) % len(PLAYER_SYMBOLS)]
        self.players.append(self)
        self.player_id = self.n
        self.n += 1

    # Player -> None
    # Clear the Players list
    def clear_players_list(self):
        self.players = []

# Human Player
class User(Player):

    # Board -> None
    # Handle user's move
    def play(self, board):
        moved = False
        while not moved:
            move = input('Enter your move as 2 numbers:\n\tFirst the column then the row: ').split()
            try:
                col = int(move[0])
                row = int(move[1])
                if is_legal_move(board, col, row, self):
                    board.update_col_row(self.symbol, col, row)
                    moved = True
            except:
                print('Please enter 2 coordinates between 0 to 2')

# Easy to beat AI Player
class Easy(Player):

    # Player, Board -> None
    # Notify the user that Easy is about to make its move
    # before making an Easy move
    def play(self, board):
        print('Easy AI turn:')
        self.play_easy(board)

    # Player, Board -> None
    # Play on a random empty cell on the Board
    def play_easy(self, board):
        coordinates = choice(board.empty_cells_indexes())
        col = coordinates[0]
        row = coordinates[1]
        board.update_col_row(self.symbol, col, row)

# Medium difficulty to beat AI Player
class Medium(Easy):

    # Player, Board -> None
    # Notify the user that Medium is about to make its move
    # Determine whether to make an Easy or Medium move and makes a move
    def play(self, board):
        print('Medium AI turn:')
        if not self.play_medium(board):
            self.play_easy(board)

    # Player, Board, char -> [int, int] or None
    # If symbol (X or O) can win in one move, return [col, row] of the winning move
    # Else, return None
    def win(self, test_board, symbol):
        for cell in test_board.empty_cells_indexes():
            test_board.update_col_row(symbol, col=cell[0], row=cell[1])
            if check_win(test_board, symbol):
                col = cell[0]
                row = cell[1]
                return cell
            test_board.update_col_row(test_board.empty_cell, cell[0], cell[1])
        # Couldn't find a win
        return None

    # Player, Board -> boolean
    # If this Player can win following current move or
    # can prevent opponent from winning next move
    # play accordingly and return True. Otherwise return False.
    def play_medium(self, board):
        # Create a new board for testing:
        test_board = Board()
        test_board.cells = copy.deepcopy(board.cells)
        move = self.win(test_board, self.symbol)
        if move:
            board.update_col_row(self.symbol, move[0], move[1])
            return True
        else:
            move = self.win(board, opponent_symbol(self.symbol))
            if move:
                board.update_col_row(self.symbol, move[0], move[1])
                return True
            else:
                return False


# Impossible to beat AI Player!
class Impossible(Medium):

    # Impossible, Board -> None
    # Determine whether to make a Medium or Impossible move and makes a move
    def play(self, board):
        print('Impossible AI turn:')
        # Check if either Player can win in the next move
        # and play to win/block opponent from winning next move
        if not self.play_medium(board):
            # Otherwise plays Impossible move
            self.play_impossible(board)

    # Impossible, Board -> None
    # Makes a move as Impossible to beat AI
    def play_impossible(self, board):
        test_board = Board()
        test_board.cells = copy.deepcopy(board.cells)

        # Use minimax algorithm to determine next move
        next_moves = []
        next_moves_values = []
        if self.symbol == 'X':
            val = X_MINIMAX
        elif self.symbol == 'O':
            val = O_MINIMAX

        for [col, row] in test_board.empty_cells_indexes():
            # Get the minimax value of playing the next empty cell on the test_board
            test_board.update_col_row(self.symbol, col, row)
            minimax_val = minimax(test_board, opponent_symbol(self.symbol))
            # Clear move from the test_board
            test_board.update_col_row(test_board.empty_cell, col, row)
            next_moves.append([col, row])
            next_moves_values.append(minimax_val)
            # Stop checking more possible moves if Minimax has found one
            # that can prevent the opponent from winning (trimming)
            if self.symbol == 'X':
                if minimax_val == X_MINIMAX:
                    break
            elif self.symbol == 'O':
                if minimax_val == O_MINIMAX:
                    break

        # Return the next best move according to minimax
        if self.symbol == 'X':
            index = next_moves_values.index(max(next_moves_values))
        else:  # Symbol is O
            index = next_moves_values.index(min(next_moves_values))
        board.update_col_row(self.symbol, next_moves[index][0], next_moves[index][1])


# ============= Minimax =============


# Board, char -> int or None
# Recursive function based on the Minimax algorithm:
# 'X' is the max and 'O' the min
def minimax(test_board, current_player_symbol):
    # stopping conditions:
    if check_win(test_board, 'X') > 0:
        return X_MINIMAX
    elif check_win(test_board, 'O') > 0:
        return O_MINIMAX
    elif test_board.full():
        return 0
    else:
        # If none of the stopping conditions had met:
        next_moves_values = []

        for [col, row] in test_board.empty_cells_indexes():
            # Trying a move on the next empty cell on the test_board:
            test_board.update_col_row(current_player_symbol, col, row)
            next_moves_values.append(minimax(test_board, opponent_symbol(current_player_symbol)))
            # Clear the move from the test_board
            test_board.update_col_row(test_board.empty_cell, col, row)

            # Trimming the Minimax tree
            if current_player_symbol == 'X':
                if next_moves_values[-1] == X_MINIMAX:
                    break
            else:  # Player is O
                if next_moves_values[-1] == O_MINIMAX:
                    break

        # Return this move's Minimax value:
        if current_player_symbol == 'X':
            return max(next_moves_values)
        elif current_player_symbol == 'O':
            return min(next_moves_values)
        else:
            print('error: undefined player symbol')
            return


# ============= Errors handling =============

# list of strings -> boolean
# Return True for legal input and False for illegal input
def legal_command(args):
    if args[0] in COMMANDS:
        if len(args) == COMMAND_LEN + NUMBER_OF_PLAYERS:
            if args[0] == 'start':
                if all(is_legal_player_type(x) for x in args[1:len(args)]):
                    return True
                else:
                    print('Illegal command')
                    return False
        elif args[0] == 'exit' and len(args) == COMMAND_LEN:
            return True
    print('Illegal command')
    return False


# char -> boolean
# Return True for legal Player symbol and False otherwise
def is_legal_player_symbol(symbol):
    return symbol in PLAYER_SYMBOLS


# string -> boolean
# Return True for legal Player type and False otherwise
def is_legal_player_type(player):
    return player in PLAYER_TYPES


# Board, int, Player -> boolean
# Return True if the move is legal and False otherwise
def is_legal_move(board, col, row, player):
    try:
        col = int(col)
        row = int(row)
    except:
        print("Please enter numbers only.")
        return False
    for val in [col, row]:
        if not 0 <= val <= 2:
            print("Please enter 2 coordinates from 0 to 2.")
            return False
    if not board.is_empty(col, row):
        print("This cell is occupied :( Please choose another one.")
        return False
    return True


# ============= Helper functions =============


# None -> list of strings or None
# Prompt the user to enter a command
# Return the command as a list if legal and None if not
def get_menu_command():
    command = input(INSTRUCTIONS_MESSAGE + '\n').split()
    if legal_command(command):
        return command
    else:
        return None


# string -> Player or None
# Create and return a Player, the Player's class is determined by player_type
# If player_type isn't a legal type return None
def new_player(player_type):
    if player_type == 'easy':
        return Easy()
    elif player_type == 'user':
        return User()
    elif player_type == 'medium':
        return Medium()
    elif player_type == 'impossible':
        return Impossible()
    else:
        return None

# Board, char -> int
# return a positive number if symbol won
def check_win(board, symbol):
    # count wins
    wins = 0
    # horizontal
    for row in board.cells:
        if all(val == symbol for val in row):
            wins += 1

    # vertical
    for i in range(board.board_size):
        if all(board.cells[j][i] == symbol for j in range(board.board_size)):
            wins += 1

    # diagonal
    if all(board.cells[i][i] == symbol for i in range(board.board_size)):
        wins += 1
    if all(board.cells[i][board.board_size - i - 1] == symbol for i in range(board.board_size)):
        wins += 1

    return wins


# Board -> boolean
# Return true if the game is over
def check_game_over(board):
    status = ""

    x_wins = check_win(board, 'X')
    o_wins = check_win(board, 'O')

    # summarize wins
    if (x_wins > 0) and (o_wins > 0):
        status = "Impossible"
    elif x_wins == 0:
        if o_wins > 0:
            status = "O wins\n"
        else:
            if not board.full():
                status = "Game not finished"
            else:
                status = "Draw"
    elif o_wins == 0:
        status = "X wins\n"
    if not status == "Game not finished":
        print(status)
    return not status == "Game not finished"


# Player -> char
# Returns the other Player's symbol
def opponent_symbol(symbol):
    if symbol == 'X':
        return 'O'
    else:
        return 'X'


# ============= Let the games begin! =============

print('''Welcome to Lihi's Tic Tac Toe game!
    ''' + PLAYERS_MESSAGE + '\n')

command = None
menu = True

while menu:
    # Game menu active
    command = get_menu_command()
    while not command:
        command = get_menu_command()
    if command[0] == 'start':

        # Set a game round
        board = Board()
        turn = Turn()
        board.print_board()

        for i in range(COMMAND_LEN, len(command)):
            new_player(command[i])

        # Game round is active
        while not check_game_over(board):
            Player.players[turn.get()].play(board)
            turn.change()
            board.print_board()

        # When game over, clear the list of Players
        Player.clear_players_list(Player)

    # Exit
    elif command[0] == 'exit':
        menu = False
    else:
        print('Error')
