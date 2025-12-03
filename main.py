import pygame
from matriz import *
from inicio import *

pygame.init()


# --- Pantalla principal ---
dimension_pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("Mi Sudoku")
fondo = pygame.image.load("fondo.sudoku.jpg")
fondo = pygame.transform.scale(fondo, (800, 600))

def pedir_nick(pantalla):
    """
    DESCRIPCION:
        Abre una pantalla donde el usuario escribe su nombre (nick). Se muestra un fondo y el texto “Ingresá tu Nick”. El usuario escribe caracteres y confirma con Enter.

    PARAMETROS:
        pantalla: superficie de Pygame donde se dibuja.

    RETORNA:
        nick (str): el nombre escrito por el jugador.
    """
    fondo = pygame.image.load("fondo.sudoku.jpg")
    fondo = pygame.transform.scale(fondo, (800, 600))

    fuente = pygame.font.Font(None, 50)
    nick = ""
    escribiendo = True

    while escribiendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nick != "":
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nick = nick[:-1]
                else:
                    if len(evento.unicode) == 1:
                        nick += evento.unicode

        # Dibujar fondo en vez del color negro
        pantalla.blit(fondo, (0, 0))

        texto = fuente.render("Ingresá tu Nick:", True, (0, 0, 0))   # texto negro
        pantalla.blit(texto, (200, 200))
        x_nick = 200 + texto.get_width() + 20

        nick_texto = fuente.render(nick, True, (0, 0, 0))  # nombre en negro
        pantalla.blit(nick_texto, (x_nick, 200))

        pygame.display.update()

    return nick

def guardar_puntaje(nick, puntaje):
    """
    DESCRIPCION:
       Guarda el puntaje del jugador en un archivo de texto plano (puntajes.txt). 

    PARAMETROS:
        nick (str): nombre del jugador.
        puntaje (int): puntos obtenidos.

    RETORNA:
        nada
    """
    with open("puntajes.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{nick} : {puntaje}\n")

def dibujar_tablero(pantalla):
    """
    DESCRIPCION:
        Dibuja el tablero de Sudoku en pantalla:
            Líneas finas para las celdas.
            Líneas gruesas cada 3 filas/columnas marcando regiones 3x3. 

    PARAMETROS:
        pantalla: superficie sobre la que se dibuja.

    RETORNA:
        nada
    """
    color_linea_fina = (200, 200, 200)
    color_linea_gruesa = (0, 0, 0)
    tamaño_celdas = 50
    inicio_x = 175
    inicio_y = 75

    for i in range(10):
        pygame.draw.line(pantalla, color_linea_fina,
                         (inicio_x, inicio_y + i * tamaño_celdas),
                         (inicio_x + tamaño_celdas*9, inicio_y + i * tamaño_celdas), 1)
        pygame.draw.line(pantalla, color_linea_fina,
                         (inicio_x + i * tamaño_celdas, inicio_y),
                         (inicio_x + i * tamaño_celdas, inicio_y + tamaño_celdas*9), 1)

    for i in range(0, 10, 3):
        pygame.draw.line(pantalla, color_linea_gruesa,
                         (inicio_x, inicio_y + i * tamaño_celdas),
                         (inicio_x + tamaño_celdas*9, inicio_y + i * tamaño_celdas), 4)
        pygame.draw.line(pantalla, color_linea_gruesa,
                         (inicio_x + i * tamaño_celdas, inicio_y),
                         (inicio_x + i * tamaño_celdas, inicio_y + tamaño_celdas*9), 4)

def dibujar_puntaje(pantalla, puntaje):
    """
    DESCRIPCION:
        Dibuja el puntaje actual en esquina superior izquierda. 

    PARAMETROS:
        pantalla: superficie de Pygame.
        puntaje (int): puntos del jugador..

    RETORNA:
        nada
    """    
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render(f"Puntos: {puntaje}", True, (0, 0, 0))
    pantalla.blit(texto, (15, 15))  # posición (x, y)

def dibujar_numeros(pantalla, matriz):
    """
    DESCRIPCION:
        Dibuja todos los números de la matriz del Sudoku:
            Negro si es número fijo del tablero original.
            Azul si lo ingresó el usuario.
            Rojo si tiene error después de validar. 

    PARAMETROS:
        pantalla: superficie donde dibujar.
        matriz (lista 9x9): estado actual del tablero.

    RETORNA:
        nada
    """    
    fuente = pygame.font.Font(None, 40)
    tamaño_celdas = 50
    inicio_x = 175
    inicio_y = 75

    for fila in range(9):
        for col in range(9):
            numero = matriz[fila][col]
            if numero != 0:
                if errores_celdas[fila][col]:
                    color = (255, 0, 0)       # rojo → número mal ingresado
                elif tablero_inicial[fila][col] != 0:
                    color = (0, 0, 0)         # negro → número fijo
                else:
                    color = (0, 0, 255)       # azul → número ingresado por el usuario
                texto = fuente.render(str(numero), True, color)
                x = inicio_x + col * tamaño_celdas + tamaño_celdas//2 - texto.get_width()//2
                y = inicio_y + fila * tamaño_celdas + tamaño_celdas//2 - texto.get_height()//2
                pantalla.blit(texto, (x, y))

def dibujar_seleccion(pantalla, celda):
    """
    DESCRIPCION:
        Dibuja un borde alrededor de la celda actualmente seleccionada.

    PARAMETROS:
        pantalla: superficie donde dibujar.
        celda (tuple (fila, col) o None).

    RETORNA:
        nada
    """
    if celda:
        fila, col = celda
        # Si la celda tiene error después de VALIDAR → rojo
        if errores_celdas[fila][col]:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)
        
        pygame.draw.rect(pantalla, color, (175 + col*50, 75 + fila*50, 50, 50), 3)

def dibujar_botones(pantalla, sudoku_listo):
    """
    DESCRIPCION:
        Dibuja los botones que existen en el dict global botones.

    PARAMETROS:
        pantalla: superficie donde dibujar.

    RETORNA:
        botones: diccionario con los rectángulos de cada botón.
    """
    fuente = pygame.font.Font(None, 40)
    BLANCO = (255,255,255)
    NEGRO = (0,0,0)

    for texto, rect in botones.items():

        if texto == "Terminar" and not sudoku_listo:
            continue

        pygame.draw.rect(pantalla, BLANCO, rect)
        texto_render = fuente.render(texto, True, NEGRO)
        pantalla.blit(texto_render, (rect.x + 20, rect.y + 10))

    return botones

def validar_tablero_completo(matriz):
    """
    DESCRIPCION:
        Valida todas las celdas que NO son del tablero inicial.
        Marca errores en errores_celdas.
        Devuelve la cantidad total de errores encontrados.

    PARAMETROS:
        matriz (lista 9x9): tablero actual del jugador.

    RETORNA:
        errores (int): cantidad total de celdas incorrectas.
    """
    global errores_celdas
    errores = 0

    for fila in range(9):
        for col in range(9):
            # Solo validamos números que NO son del tablero original
            if tablero_inicial[fila][col] == 0:
                num = matriz[fila][col]

                if num != 0 and not validar_numero(matriz, fila, col, num):
                    errores_celdas[fila][col] = True
                    errores += 1
                else:
                    errores_celdas[fila][col] = False

    return errores

#  Mostrar pantalla de inicio 
accion, nivel = mostrar_inicio()
if accion == "Salir":
    pygame.quit()
    quit()

# Definir dificultad 
if nivel == "Fácil":
    numeros_por_region = 5
elif nivel == "Medio":
    numeros_por_region = 3
elif nivel == "Difícil":
    numeros_por_region = 2
else:
    numeros_por_region = 5  

#  Crear tablero 
tablero_inicial = generar_tablero_facil_por_region(numeros_por_region)
matriz = [fila.copy() for fila in tablero_inicial]
errores_celdas = [[False]*9 for _ in range(9)]
regiones_completadas = [[False]*3 for _ in range(3)]
botones = {
    "Validar": pygame.Rect(500, 540, 230, 50),
    "Reiniciar": pygame.Rect(70, 540, 230, 50),
    "Terminar": pygame.Rect(500, 10, 230, 50),
    "Volver": pygame.Rect(200, 10, 230, 50)
}

celda_incorrecta = False
celda_seleccionada = None
puntaje = 0


# ------------------- LOOP PRINCIPAL -------------------------

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = evento.pos            
            # Selección de celda   
            if 175 <= mouseX <= 625 and 75 <= mouseY <= 525:   
                fila = (mouseY - 75) // 50 
                columna = (mouseX - 175) // 50 
                celda_seleccionada = (fila, columna)   
                celda_incorrecta = False                           
            if botones["Validar"].collidepoint(mouseX, mouseY):                
                errores = validar_tablero_completo(matriz) 
                puntaje -= errores             
                # Si hay errores, se muestran pero NO se sale del tablero  
                if errores > 0:
                    continue                       
                # Verificar si el sudoku está completo (sin ceros) 
                sudoku_completo = True 
                for f in range(9): 
                    for c in range(9): 
                        if matriz[f][c] == 0:  
                            sudoku_completo = False            
                # Si no está completo → no pasar al ingreso de nick
                if not sudoku_completo:
                    continue                       
                # Si NO hay errores y el tablero está completo:
                nick = pedir_nick(dimension_pantalla)  
                guardar_puntaje(nick, puntaje)             
                # Volver al inicio 
                accion, nivel = mostrar_inicio()               
                if accion == "Salir":  
                    pygame.quit()  
                    quit()             
                # Reajustar dificultad 
                if nivel == "Fácil":   
                    numeros_por_region = 5 
                elif nivel == "Medio": 
                    numeros_por_region = 3 
                else:  
                    numeros_por_region = 2             
                tablero_inicial = generar_tablero_facil_por_region(numeros_por_region) 
                matriz = [fila.copy() for fila in tablero_inicial] 
                puntaje = 0
                celda_seleccionada = None              
            # --- REINICIAR TABLERO ---
            if botones["Reiniciar"].collidepoint(mouseX, mouseY):  
                tablero_inicial = generar_tablero_facil_por_region(numeros_por_region) 
                matriz = [fila.copy() for fila in tablero_inicial] 
                puntaje = 0
                celda_seleccionada = None
            if botones["Terminar"].collidepoint(mouseX, mouseY):
                nick = pedir_nick(dimension_pantalla)
                guardar_puntaje(nick, puntaje)
                # Volver al inicio
                accion, nivel = mostrar_inicio()
                if accion == "Salir":  
                    pygame.quit()  
                    quit()             
                # Reajustar dificultad 
                if nivel == "Fácil":   
                    numeros_por_region = 5 
                elif nivel == "Medio": 
                    numeros_por_region = 3 
                else:  
                    numeros_por_region = 2             
                tablero_inicial = generar_tablero_facil_por_region(numeros_por_region) 
                matriz = [fila.copy() for fila in tablero_inicial] 
                puntaje = 0
                celda_seleccionada = None
            if botones["Volver"].collidepoint(mouseX, mouseY):
                accion, nivel = mostrar_inicio()
    
                if accion == "Salir":
                    pygame.quit()
                    quit()

                # Si vuelve a "Jugar", regenerar tablero con la dificultad elegida
                if nivel == "Fácil":
                    numeros_por_region = 5
                elif nivel == "Medio":
                    numeros_por_region = 4
                else:
                    numeros_por_region = 3

                tablero_inicial = generar_tablero_facil_por_region(numeros_por_region)
                matriz = [fila.copy() for fila in tablero_inicial]
                puntaje = 0
                celda_seleccionada = None
                errores_celdas = [[False]*9 for _ in range(9)]
                regiones_completadas = [[False]*3 for _ in range(3)]



        elif evento.type == pygame.KEYDOWN and celda_seleccionada:
            fila, col = celda_seleccionada
            if tablero_inicial[fila][col] == 0:
                if evento.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    matriz[fila][col] = 0
                    celda_incorrecta = False               
                elif evento.unicode in "123456789":
                    numero = int(evento.unicode)
                    matriz[fila][col] = numero
                    errores_celdas[fila][col] = False
                    # Validación inmediata
                    if validar_numero(matriz, fila, col, numero):
                        celda_incorrecta = False
                        puntaje = actualizar_puntaje(puntaje, matriz, fila, col, numero, celda_incorrecta)
                        puntaje = actualizar_puntaje_regiones(matriz, regiones_completadas, puntaje)
                    else:
                        celda_incorrecta = True
                        puntaje = actualizar_puntaje(puntaje, matriz, fila, col, numero, celda_incorrecta)

                        

    dimension_pantalla.blit(fondo, (0,0))
    dibujar_tablero(dimension_pantalla)
    dibujar_numeros(dimension_pantalla, matriz)
    dibujar_seleccion(dimension_pantalla, celda_seleccionada)
    
    sudoku_listo = True
    for fila in range(9):
        for col in range(9):
            if matriz[fila][col] == 0:
                sudoku_listo = False
            if errores_celdas[fila][col]:
                sudoku_listo = False

    dibujar_botones(dimension_pantalla, sudoku_listo)
    dibujar_puntaje(dimension_pantalla, puntaje)

    pygame.display.update()
