import time
import random
import numpy as np

def createBoard(x,y):
    '''
    createBoard generates an array of zeros for conect4
    
    Parameters
    ----------
    x : int
        number of rows.
    y : int
        number of columns.

    Returns
    -------
    A board of x rows for y columns.

    '''
    board = np.zeros((x,y))
    return board

def moveValidation(board, column):
    '''
    moveValidation evaluate when move is valid or not

    Parameters
    ----------
    board : array
        DESCRIPTION.
    column : int
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    return board[0,column] == 0

def getRow(board, column):
    for row in reversed(range(rows)):
        if board[row,column] == 0:
            return row 

while 0 in board[0]: 
    turn +=1
    if (turn % 2) != 0:
    # Player 1 turn
        # playerTurn()
        column = int(input('P1 Selecciona una columna (0-6): '))
        if moveValidation(board, column):        
            row = getRow(board, column)
            board[row,column] = 1
            print(board)
            games
        else:
            column = int(input('La columna esta llena, selecciona otra columna (0-6): '))
        
    else:
    # Player 2 turn
        # playerTurn()
        column = int(input('P2 Selecciona una columna (0-6): '))
        if moveValidation(board, column):        
            row = getRow(board, column)
            board[row,column] = -1
            print(board)
        else:
            column = int(input('La columna esta llena, selecciona otra columna (0-6): '))