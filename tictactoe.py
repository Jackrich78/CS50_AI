"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Start with X
    Alternate between the 2 players 
    """
    X = 0
    O = 0

    # TODO check terminal state
    # if terminal == True:
    #    return X

    # iterate over rows
    for row in board:
        for cell in row:
            if cell == "X":
                X += 1
            elif cell == "O":
                O += 1

    if X > O:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    use the tuple to find out which coordinates are still empty
    Any return value is acceptable for all empty coords 
    """
    possible_actions = set()

    # iterate over rows
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Make a deep copy of the board first
    """
    if action is None or not isinstance(action, tuple) or len(action) != 2:
        raise ValueError("Invalid action")
    
    # check move is valid
    i, j = action 
    if i < 0 or i >= len(board) or j < 0 or j >= len(board[i]):
        raise ValueError("Acount out of bounds")

    # checks board and action
    print("Board before action:", board)
    print("Action being applied:", action)
    if board[action[0]][action[1]] is not None:
        raise Exception ("Cell or Board full")
    
    current_player = player(board)
    new_board_state = copy.deepcopy(board)
    
    # add action to a copy of the current board
    new_board_state[action[0]][action[1]] = current_player

    return new_board_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontal rows for a winner
    for row in board:
        if len(set(row)) == 1 and row[0] is not None:
            return row[0]
    
    # check vertical columns for a winner
    for j in range(len(board[0])):
        column = [board[i][j] for i in range(len(board))]
        if len(set(column)) == 1 and column[0] is not None:
            return column[0]

    # check diagonals
    if len(set([board[0][0], board[1][1], board[2][2]])) == 1 and board[0][0] is not None:
        return board[0][0]
    if len(set([board[0][2], board[1][1], board[2][0]])) == 1 and board[0][2] is not None:
        return board[0][2]
    
    # if no winner is found return None
    return None


"""
# Example usage
board = [
    ["X", "O", "X"],
    ["O", "O", "X"],
    ["X", "O", None]
]
print("is there a winner:", winner(board))
"""

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check if there is a winner
    if winner(board) is not None:
        # print("terminal board sate:", board)
        return True
    
    # check if all cells are filled
    for row in board:
        for cell in row:
            if cell is EMPTY: # or None?
                # print("terminal board sate:", board)
                return False
            
    # it's a draw if there are not empty cells and no winner
    # print("terminal board sate:", board)
    return True

# print("is board terminal:", terminal(board))

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0

# print("utility:", utility(board))

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # check whos turn it is
    if player(board) == X:
        # _ is used ti ignore part of the variable. We on;ly care about the move here. 
        # alpha, beta pruning variables added to function
        _, optimal_move = maximize(board, float('-inf'), float('inf')) 
    else:
        _, optimal_move = minimize(board, float('-inf'), float('inf'))

    return optimal_move

def maximize(board, alpha, beta):
    """
    Find the optimal move maximizing the utility for 'X'.
    """
    # if board is terminal return just the utility score
    if terminal(board):
        return utility(board), None

    highest_utility = float('-inf')
    best_move = None
    for action in actions(board):
        # for each possible action calculate the utility of the board after that action
        score, _ = minimize(result(board, action), alpha, beta)
        # update utility if a better move is found
        if score > highest_utility:
            highest_utility = score
            best_move = action
        # update alpha to be the maximum of itself and the new score
        alpha = max(alpha, score)
        #if alpha becomes grater than beta prune remaining branches at that node
        if beta <= alpha:
            break # beta cut-off
    
    # return best utility and corresponding move
    return highest_utility, best_move

def minimize(board, alpha, beta):
    """
    Find the optimal move minimizing the utility for 'O'.
    """
    if terminal(board):
        return utility(board), None

    lowest_utility = float('inf')
    best_move = None
    for action in actions(board):
        score, _ = maximize(result(board, action), alpha, beta)
        if score < lowest_utility:
            lowest_utility = score
            best_move = action
        beta = min(beta, score)
        if beta <= alpha:
            break # Alpha cut-off

    return lowest_utility, best_move
