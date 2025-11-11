import pygame



pygame.init()
pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("Sudoku")

NEGRO = (0,0,0)
BLANCO = (255,255,255)

fondo = pygame.image.load("fondo.sudoku.jpg")
fondo = pygame.transform.scale(fondo, (800, 600))
# Tamaño de cada cuadrado
TAM_CUADRO = 40


# Margen inicial para centrar la grilla
MARGEN_X = 200
MARGEN_Y = 100

while True:
    for evento in pygame.event.get():
          if evento.type == pygame.QUIT:
               pygame.quit()
               quit()

    #pantalla.fill((0,0,0))

    color = (255, 255, 255)

    pantalla.blit(fondo, (0, 0))

    #for fila in range(9):
        #for col in range(9):
            #x = MARGEN_X + col * TAM_CUADRO
            #y = MARGEN_Y + fila * TAM_CUADRO
            #pygame.draw.rect(pantalla, BLANCO, (x, y, TAM_CUADRO, TAM_CUADRO), 1)
    for i in range(10):
        grosor = 5 if i % 3 == 0 else 1  # cada 3 líneas, más grueso
    # Líneas horizontales
        pygame.draw.line(pantalla, BLANCO, (MARGEN_X, MARGEN_Y + i * TAM_CUADRO), (MARGEN_X + 9 * TAM_CUADRO, MARGEN_Y + i * TAM_CUADRO),  grosor)
    # Líneas verticales
        pygame.draw.line(pantalla, BLANCO, (MARGEN_X + i * TAM_CUADRO, MARGEN_Y),(MARGEN_X + i * TAM_CUADRO, MARGEN_Y + 9 * TAM_CUADRO), grosor)



    VERDE = (0, 255, 0)
    coordenadas = (30, 30, 130, 70)
    #rectangulo = pygame.draw.rect(pantalla, VERDE, coordenadas)
    fuente = pygame.font.Font(None, 40)
    botones = {
    "Validar": (550, 500, 200, 50),
    "Reiniciar": (50, 500, 200, 50)
    }
    for texto, coord in botones.items():
        rect = pygame.draw.rect(pantalla, BLANCO, coord)
        texto_render = fuente.render(texto, True, NEGRO)
        pantalla.blit(texto_render, (coord[0] + 20, coord[1] + 10))

    pygame.display.flip()