import pygame
from car import Car

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

car = Car(226, 111, -90, ai=True)
track = pygame.image.load("track.png")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    car.update(dt, track, (255, 255, 255, 255))

    # draw 
    screen.blit(track, (0, 0))
    car.draw(screen)
    pygame.display.flip()

    if not car.alive:
        car = Car(226, 111, -90, ai=True)

    dt = clock.tick(60) / 1000

pygame.quit()