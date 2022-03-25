import pygame
import sys
import math
import random

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()


def distance_to(pos_1, pos_2):
    return math.sqrt((pos_2[0] - pos_1[0]) ** 2 + (pos_2[1] - pos_1[1]) ** 2)


def angle_to(pos_1, pos_2):
    return math.atan2(pos_2[1] - pos_1[1], pos_2[0] - pos_1[0])


def get_movement(angle, speed):
    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed

    return dx, dy


class Particle:
    distance_retention = 60

    def __init__(self, x, y, speed=0.5, size=7):
        self.pos = [x, y]
        self.speed = speed
        self.size = size

    def update(self, mouse_pos, dt):
        if distance_to(self.pos, mouse_pos) < self.distance_retention:
            angle = angle_to(self.pos, mouse_pos)
            dx, dy = get_movement(angle, self.speed)
            self.pos[0] -= dx * dt
            self.pos[1] -= dy * dt

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.pos, self.size)


number_of_particles = 300
gen_random_pos = lambda: (random.randrange(0, 500) for _ in range(number_of_particles))
particles = [Particle(x, y) for x, y in zip(gen_random_pos(), gen_random_pos())]
while (run := True):
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    dt = clock.tick() / 1000
    dt *= 60
    screen.fill(0)

    for particle in particles:
        particle.update(mouse_pos, dt)
        particle.draw(screen)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()