import pygame

pygame.init()
pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("Sudoku")

fondo = pygame.image.load("fondo.sudoku.jpg")
fondo = pygame.transform.scale(fondo, (800, 600))

NEGRO = (0, 0, 0)


while True:
    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

    VERDE = (0, 255, 0)
    coordenadas = (30, 30, 130, 70)
    #rectangulo = pygame.draw.rect(pantalla, VERDE, coordenadas)
    fuente = pygame.font.Font(None, 40)
    botones = {
    "Nivel": (300, 200, 200, 50),
    "Jugar": (300, 270, 200, 50),
    "Ver Puntajes": (300, 340, 200, 50),
    "Salir": (300, 410, 200, 50)
    }
    for texto, coord in botones.items():
        rect = pygame.draw.rect(pantalla, VERDE, coord)
        texto_render = fuente.render(texto, True, NEGRO)
        pantalla.blit(texto_render, (coord[0] + 20, coord[1] + 10))
    
    for evento in pygame.event.get():
        if evento.type == pygame.MOUSEBUTTONDOWN:
            posicion = (evento.pos)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    print("Clic izquierdo detectado.")
                elif evento.button == 3:
                    print("Clic derecho detectado.")
         
    
    
    
    
    pygame.display.flip()