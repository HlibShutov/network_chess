import pygame

def chessboard(display, color1, color2):
    display.fill((0, 0, 0))
    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(display, color2 if (j+i)%2 else color1, (j*50, i*50, 50, 50))
    pygame.display.flip()