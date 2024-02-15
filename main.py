import pygame
from car import Car
import time

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
generation = 0
font = pygame.font.Font(None, 36)

cars = [Car(226, 111, -90, ai=True) for i in range(10)]
track = pygame.image.load("track.png")

while running:
    generation_alive = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    for car in cars:
        if car.alive:
            car.update(dt, track, (255, 255, 255, 255))
            generation_alive = generation_alive or car.alive

    # draw 
    screen.blit(track, (0, 0))
    for car in cars:
        if car.alive:
            car.draw(screen)

    generation_text = font.render(f'GENERATION: {generation}', True, (0, 0, 255))
    screen.blit(generation_text, (10, 10))  # Blit the text to the screen at position (10, 10)


    # check if generation is dead
    if not generation_alive:
        generation += 1
        ## find the best 'brain'
        best_fitness = cars[0].get_fitness()
        best_brain = cars[0].brain

        for car in cars:
            if car.get_fitness() > best_fitness:
                best_fitness = car.get_fitness()
                best_brain = car.brain
        
        cars = []
        
        for i in range(10):
            car = Car(226, 111, -90, ai=True)
            car.brain = best_brain.mutate(1)
            cars.append(car)

    pygame.display.flip()


    dt = clock.tick(60) / 1000

pygame.quit()