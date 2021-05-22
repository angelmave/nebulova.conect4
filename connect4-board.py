# =============================================================================
# Connect4 Board
# =============================================================================
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

board = np.zeros((6,7))


def conect4():
    '''
    conect4 runs the game

    Parameters
    ----------
    def conect4 : TYPE
        DESCRIPTION.

    Returns
    -------
    Enterteinment.

    '''
    print('''Conecta 4
          Opciones
          1. Un Jugador VS CPU
          2. Dos Jugadores
          3. CPU VS CPU
          4. Scores
          ''')
    mode = int(input('Selecciona un modo de juego: '))
    if mode == 1:
        player1 = input('Nombre del primer Jugador: ')
        player2 = CPU
    elif mode == 2:
        player1 = input('Nombre del primer Jugador: ')
        player2 = input('Nombre del segundo Jugador: ')
    elif mode == 3:
        player1 = CPU
        player2 = CPU
    
    print('''Selecciona un Tablero:
          1. 6x7
          2. Personalizado
          ''')
    boardSize = int(input('Selecciona un tablero: '))
    if boardSize == 2:
        rows = int(input('Indica el número de fila: '))
        columns = int(input('Indica el número de columnas: '))
    else:
        rows = 6
        columns = 7
    board = createBoard(rows,columns)


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
    
def winnerValidation(board):    
    # checkVer
    for column in range(board.shape[:,columns]):
        if sum(board[column]) == 4:
            winner = player1
        else sum(board[column]) == -4:
            winner = player2
    # checkHor
    for row in range(board.shape[:,rows]):
        if sum(board[row]) == 4:
            winner = player1
        else sum(board[row]) == -4:
            winner = player2
    # checkDiag
    for diag in range(board.shape[:,rows]):
        if sum(board[diag]) == 4:
            winner = player1
        else sum(board[diag]) == -4:
            winner = player2