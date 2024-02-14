import pygame
from car import Car

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

car = Car(640, 360, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('white')
    car.draw(screen)
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()