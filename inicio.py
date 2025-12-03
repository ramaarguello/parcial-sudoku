import pygame

fondo = pygame.image.load("fondo.sudoku.jpg")
fondo = pygame.transform.scale(fondo, (800, 600))


def cargar_puntajes():

    """
    DESCRIPCION:
        Lee el archivo 'puntajes.txt' y carga todos los puntajes guardados.
        Cada línea del archivo debe tener el formato: 'nombre : puntaje'.
        Convierte los puntajes en enteros y los devuelve como una lista.

    RETORNA:
        puntajes (list[tuple[str, int]]):
            Lista de tuplas donde cada elemento contiene:
            - nombre (str)
            - puntaje (int)
    """

    puntajes = []

    with open("puntajes.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if ":" in linea:
                nombre, puntaje = linea.strip().split(" : ")
                puntaje = int(puntaje)  
                puntajes.append((nombre, puntaje))

    return puntajes

def mejores_cinco(puntajes):
    
    """
    DESCRIPCION:
        Recibe una lista de puntajes y devuelve únicamente los cinco mejores.
        Los puntajes se ordenan de mayor a menor según el valor numérico.

    PARAMETROS:
        puntajes (list[tuple[str, int]]):
            Lista de tuplas con (nombre, puntaje).

    RETORNA:
        list[tuple[str, int]]:
            Lista con los cinco puntajes más altos.
            Si hay menos de cinco, devuelve todos los disponibles.
    """

    puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)
    return puntajes_ordenados[:5]

def mostrar_puntajes(pantalla):
    
    """
    DESCRIPCION:
        Despliega una pantalla que muestra los mejores 5 puntajes guardados.
        Muestra:
            - Fondo del juego
            - Título "Mejores 5 puntajes"
            - Lista de nombres y puntajes
            - Botón "Volver" para regresar al menú principal

        Esta función mantiene su propio loop hasta que se hace clic en VOLVER.

    PARAMETROS:
        pantalla (pygame.Surface):
            Superficie principal donde se dibuja la interfaz.

    RETORNA:
        Nada. La función finaliza cuando el usuario presiona "Volver".
    """

    fondo = pygame.image.load("fondo.sudoku.jpg")
    fondo = pygame.transform.scale(fondo, (800, 600))

    fuente = pygame.font.Font(None, 60)
    fuente_chica = pygame.font.Font(None, 40)

    puntajes = mejores_cinco(cargar_puntajes())

    volver_boton = pygame.Rect(300, 520, 200, 50)

    en_puntajes = True
    while en_puntajes:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if volver_boton.collidepoint(evento.pos):
                    en_puntajes = False  # vuelve a la pantalla de inicio

        # DIBUJAR FONDO
        pantalla.blit(fondo, (0, 0))

        # Título
        titulo = fuente.render("Mejores 5 puntajes", True, (0, 0, 0))
        pantalla.blit(titulo, (150, 50))

        # Listado
        y = 160
        if puntajes:
            for nombre, pts in puntajes:
                texto = fuente_chica.render(f"{nombre}: {pts}", True, (0, 0, 0))
                pantalla.blit(texto, (250, y))
                y += 50
        else:
            texto = fuente_chica.render("No hay puntajes guardados", True, (0, 0, 0))
            pantalla.blit(texto, (200, 250))

        # Botón volver
        pygame.draw.rect(pantalla, (255, 255, 255), volver_boton)
        texto_volver = fuente_chica.render("Volver", True, (0, 0, 0))
        pantalla.blit(texto_volver, (volver_boton.x + 50, volver_boton.y + 10))

        pygame.display.update()

def mostrar_inicio():

    """
    DESCRIPCION:
        Muestra la pantalla de inicio del juego.
        Contiene los botones:
            - Nivel (cambia entre Fácil / Medio / Difícil)
            - Jugar (entra al tablero)
            - Ver Puntajes (abre pantalla de puntajes)
            - Salir (cierra el juego)

        Esta función mantiene un loop hasta que el usuario elige
        "Jugar" o "Salir".

    PARAMETROS:
        Ninguno.

    RETORNA:
        tuple (accion, nivel):
            accion (str):
                "Jugar" → inicia el sudoku
                "Salir" → cierra la aplicación
            nivel (str):
                "Fácil", "Medio" o "Difícil"
    """

    pantalla = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Sudoku")

    # Cargar fondo
    fondo = pygame.image.load("fondo.sudoku.jpg")
    fondo = pygame.transform.scale(fondo, (800, 600))

    blanco = (255, 255, 255)
    negro = (0,0,0)
    fuente = pygame.font.Font(None, 40)

    # Botones principales
    botones = {
        "Nivel": (300, 200, 200, 50),
        "Jugar": (300, 270, 200, 50),
        "Ver Puntajes": (300, 340, 200, 50),
        "Salir": (300, 410, 200, 50)
    }

    nivel = "Fácil"  # nivel por defecto

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "Salir", nivel

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = evento.pos
                for texto, coord in botones.items():
                    rect = pygame.Rect(coord)
                    if rect.collidepoint(mouse_pos):
                        if texto == "Jugar":
                            return "Jugar", nivel
                        elif texto == "Nivel":
                            # Cambiar nivel con cada clic
                            if nivel == "Fácil":
                                nivel = "Medio"
                            elif nivel == "Medio":
                                nivel = "Difícil"
                            else:
                                nivel = "Fácil"
                        elif texto == "Ver Puntajes":
                            mostrar_puntajes(pantalla)
                        elif texto == "Salir":
                            return "Salir", nivel

        # Dibujar fondo y botones
        pantalla.blit(fondo, (0,0))
        for texto, coord in botones.items():
            pygame.draw.rect(pantalla, blanco, coord)
            texto_render = fuente.render(texto, True, negro)
            pantalla.blit(texto_render, (coord[0] + 20, coord[1] + 10))

        # Mostrar nivel actual
        nivel_render = fuente.render(f"Nivel: {nivel}", True, negro)
        pantalla.blit(nivel_render, (300, 150))

        pygame.display.flip()
