import numpy as np

row_count =6

column_count=7

def crear_tablero():
        tablero= np.zeros((row_count, column_count))
        return tablero

def espacio_valido(tablero, col):
    return tablero[row_count-1][col]==0

def prox_fila_vacia(tablero, col):
    for r in range(row_count):
        if tablero[r][col] == 0:
            return r

def soltar_ficha(tablero, fila, col, ficha):
    tablero[fila][col] = ficha

def imprimir_tablero(tablero):
    print(np.flipud(tablero))

def mov_win(tablero, ficha):
     # buscar localizacion horizontal ganadora
     for c in range(column_count -3):
         for r in range (row_count):
             if tablero[r][c] == ficha and tablero [r][c+1] == ficha and tablero[r][c+2] == ficha and tablero[r][c+3] == ficha:
                 return True
    # buscar localizacion vertical ganadora
     for c in range(column_count):
         for r in range (row_count -3):
             if tablero[r][c] == ficha and tablero[r+1][c] == ficha and tablero[r+2][c] == ficha and tablero[r+3][c] == ficha:
                 return True
    # buscar posicion en diagonal positiva
     for c in range(column_count-3):
         for r in range (row_count -3):
             if tablero[r][c] == ficha and tablero[r+1][c+1] == ficha and tablero[r+2][c+2] == ficha and tablero[r+3][c+3] == ficha:
                 return True
             
    # buscar posicion en diagonal negativa
     for c in range(column_count-3):
         for r in range (3, row_count):
             if tablero[r][c] == ficha and tablero[r-1][c+1] == ficha and tablero[r-2][c+2] == ficha and tablero[r-3][c+3] == ficha:
                 return True
    

tablero= crear_tablero()
imprimir_tablero(tablero)

game_over, turn=False, 0

while not game_over:
    #solicitar movimiento jugador 1:
        if turn ==0:
            col= int(input("Movimiento jugador 1 (0-6):"))
            if espacio_valido(tablero, col):
                fila= prox_fila_vacia(tablero, col)
                soltar_ficha(tablero, fila, col, 1)
                imprimir_tablero(tablero)
                
                if mov_win(tablero, 1):
                    print ("Jugador 1 wins")
                    imprimir_tablero(tablero)
                    game_over= True
                    break
                    
        else:
            col= int(input("Movimiento jugador 2 (0-6):"))
            if espacio_valido(tablero, col):
                fila= prox_fila_vacia(tablero, col)
                soltar_ficha(tablero, fila, col, 2)
                imprimir_tablero(tablero)
                
                if mov_win(tablero, 2):
                    print ("Jugador 2 wins")
                    imprimir_tablero(tablero)
                    game_over= True
                    break
                
        turn +=1
        turn= turn%2

