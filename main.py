import pygame
from car import Car

GENERATION_SIZE = 10
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
INITIAL_X = 226
INITIAL_Y = 111
TRACK_IMG = 'track.png'
COLLISION_COLOR = (255, 255, 255, 255)
MUTATION_RATE = 0.3

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
generation = 0
font = pygame.font.Font(None, 36)
track = pygame.image.load(TRACK_IMG)

cars = [Car(INITIAL_X, INITIAL_Y, -90, ai=True) for i in range(10)]

while running:
    generation_alive = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    for car in cars:
        if car.alive:
            car.update(dt, track, COLLISION_COLOR)
            generation_alive = generation_alive or car.alive

    # draw 
    screen.blit(track, (0, 0))
    for car in cars:
        if car.alive:
            car.draw(screen)

    generation_text = font.render(f'GENERATION: {generation}', True, (0, 0, 255))
    screen.blit(generation_text, (10, 10))  

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
            car = Car(INITIAL_X, INITIAL_Y, -90, ai=True)
            car.brain = best_brain.mutate(MUTATION_RATE)
            cars.append(car)

    pygame.display.flip()


    dt = clock.tick(60) / 1000

pygame.quit()