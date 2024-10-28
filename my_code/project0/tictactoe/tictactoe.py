"""
Tic Tac Toe Player
"""

import math
import copy
import random
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
    """
    x_count = 0
    o_count = 0
    # count how many Xs and Os are on the board
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    
    # it is X's turn when x_count equals to o_count
    if x_count == o_count:
        return X
    else:
        return O
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allActions = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                allActions.add((i, j))
    return allActions
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # deepcopy the board
    newboard = copy.deepcopy(board)
    # out-of-bound actions
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise "action out of bounds"
    # only actions on empty cells are valid
    if newboard[action[0]][action[1]] != EMPTY:
        raise "invalid action"
    else:
        newboard[action[0]][action[1]] = player(board)
    return newboard
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # the board hasn't terminated yet, then return None
    if not terminal(board):
        return None

    # here I just list all situations
    if board[0][0] == board[0][1] and board[0][1] == board[0][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    
    if board[1][0] == board[1][1] and board[1][1] == board[1][2]:
        if board[1][0] == X:
            return X
        elif board[1][0] == O:
            return O
    
    if board[2][0] == board[2][1] and board[2][1] == board[2][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
    
    if board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    
    if board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        if board[0][1] == X:
            return X
        elif board[0][1] == O:
            return O
    
    if board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O
    
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O
    
    # the board has terminated, not because three in one line
    # then it can only be ending in a tie
    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # here I just list all situations that indicates terminal
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][0] != EMPTY:
        return True
    
    if board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][0] != EMPTY:
        return True
    
    if board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][0] != EMPTY:
        return True
    
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[0][0] != EMPTY:
        return True
    
    if board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[0][1] != EMPTY:
        return True
    
    if board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[0][2] != EMPTY:
        return True
    
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return True
    
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return True
    
    # empty cells on the board indicate game hasn't terminated yet
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    
    return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        res = winner(board)
        if res == X:
            return 1
        elif res == O:
            return -1
    return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # terminal board return None
    if terminal(board):
        return None
    
    allActions = actions(board)
    optAction = None
    
    # conduct random put when it is a new board
    if board == [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]:
        cellid = random.randint(0, 8)
        action = (cellid // 3, cellid % 3)
        return action
    
    if player(board) == X:
        optScore = -999
        for action in allActions:
            newboard = result(board, action)
            if terminal(newboard):
                score = utility(newboard)
            else:
                while not terminal(newboard):
                    newboard = result(newboard, minimax(newboard))
                score = utility(newboard)
            if score > optScore:
                optScore = score
                optAction = action
                
    if player(board) == O:
        optScore = 999
        for action in allActions:
            newboard = result(board, action)
            if terminal(newboard):
                score = utility(newboard)
            else:
                while not terminal(newboard):
                    newboard = result(newboard, minimax(newboard))
                score = utility(newboard)
            if score < optScore:
                optScore = score
                optAction = action
    
    return optAction 
    raise NotImplementedError

'''def main():
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, X, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    print(minimax(board))
    

if __name__ == "__main__":
    main()'''