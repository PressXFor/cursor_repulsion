import pygame
import pygame as pg
from numpy import sin, cos, deg2rad
import cProfile
import pstats

profiler = cProfile.Profile()

pg.init()
DISPLAY_W, DISPLAY_H = 1000, 700
surface = pg.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True

size = (0, 0, 5, 5)
testImage = pg.image.load('./testimage.png').convert_alpha()
testImage_rect = testImage.get_rect()


# create the grid of pixels
def grid():
    global particles
    global goi
    particlesize = 5

    particles = []
    goi = 0

    pg.draw.rect(surface, 'white', testImage_rect, 1)

    for x in range(DISPLAY_W):
        for y in range(DISPLAY_H):
            rect = pg.Rect(x * particlesize, y * particlesize, particlesize, particlesize)
            if testImage_rect.colliderect(rect):
                particles.append(rect)
                pygame.draw.rect(surface, 'white', rect, 1)
                goi += 1


def repulsion():

    mouseX, mouseY = pygame.mouse.get_pos()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    profiler.enable()
    grid()
    profiler.disable()
    pg.display.update()

pygame.quit()

stats = pstats.Stats(profiler).sort_stats('ncalls')
stats.print_stats()
test