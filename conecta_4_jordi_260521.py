import numpy as np
import pygame
import sys
import math

#colores básicos:
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED= (255, 0, 0)
BLUE= (0, 0, 255)
YELLOW=(255, 255, 0)

#medidas tablero
row_count =6
column_count=7

def crear_tablero():
    tablero= np.zeros((row_count, column_count))
    return tablero

def espacio_valido(tablero, col):
    return tablero[5][col]==0

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
#visualización del tablero:
             
def draw_tablero(tablero):
    for c in range (column_count):
        for r in range (row_count):
            pygame.draw.rect(screen,GREEN, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK,(int (c*SQUARESIZE+SQUARESIZE/2),int( r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range (column_count):
        for r in range (row_count):            
            if tablero[r][c] == 1:
                pygame.draw.circle(screen, BLUE,(int (c*SQUARESIZE+SQUARESIZE/2),height - int( r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif tablero[r][c] == 2:
                pygame.draw.circle(screen, RED,(int (c*SQUARESIZE+SQUARESIZE/2), height - int( r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()  
    

tablero= crear_tablero()
imprimir_tablero(tablero)

game_over, turn=False, 0

turn= 0
#inicializador de pygame, con tamaño total de la ventana de juego:
pygame.init()
SQUARESIZE = 100

#tamaño de las cuadras:
width= column_count * SQUARESIZE
height= (row_count+1) * SQUARESIZE

size= (width, height)

#tamaño de los circulos:
RADIUS= int(SQUARESIZE/2 - 5)

screen= pygame.display.set_mode(size)
draw_tablero(tablero)
pygame.display.update()
myfont= pygame.font.SysFont("monospace", 50)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, BLUE,(posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, RED,(posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()  
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            #solicitar movimiento jugador 1:
            if turn ==0:
                posx= event.pos[0]
                col= int(math.floor(posx/SQUARESIZE))
                #col= int(input("Movimiento jugador 1 (0-6):"))
            
                if espacio_valido(tablero, col):
                    fila= prox_fila_vacia(tablero, col)
                    soltar_ficha(tablero, fila, col, 1)
                    #imprimir_tablero(tablero)
                
                    if mov_win(tablero, 1):
                        label = myfont.render("Has perdido jugador 2", 1, BLUE)
                        screen.blit(label,(40, 10))
                        #print ("Jugador 1 wins")
                        #imprimir_tablero(tablero)
                        game_over= True
                        #break
                    
            else:
                posx= event.pos[0]
                col= int(math.floor(posx/SQUARESIZE))
                #col= int(input("Movimiento jugador 2 (0-6):"))
            
                if espacio_valido(tablero, col):
                    fila= prox_fila_vacia(tablero, col)
                    soltar_ficha(tablero, fila, col, 2)
                    #imprimir_tablero(tablero)
                
                    if mov_win(tablero, 2):
                        label = myfont.render("Has perdido jugador 1", 1, RED)
                        screen.blit(label,(40, 10))
                        #print ("Jugador 2 wins")
                        #imprimir_tablero(tablero)
                        game_over= True
                        #break
                    
            imprimir_tablero(tablero)
            draw_tablero(tablero)                    
                
            turn +=1
            turn= turn%2
        
            if game_over:
                pygame.time.wait(3000)

