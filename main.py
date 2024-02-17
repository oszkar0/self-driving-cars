import pygame
from car import Car
import neat

GENERATION_SIZE = 10
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
INITIAL_X = 226
INITIAL_Y = 111
TRACK_IMG = 'track2.png'
COLLISION_COLOR = (255, 255, 255, 255)
MUTATION_RATE = 0.5


def run_generation(genomes, config):
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()        
    font = pygame.font.Font(None, 36)
    track = pygame.image.load(TRACK_IMG)
    dt = 0
    running = True
    global generation
    generation += 1

    cars = []

    for index, genome in genomes:
        neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        car = Car(INITIAL_X, INITIAL_Y, neural_network=neural_network)
        cars.append(car)
        

    while running:
        generation_alive = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # update
        for index, car in enumerate(cars):
            if car.alive:
                car.update(dt, track, COLLISION_COLOR)
                genomes[index][1].fitness = car.get_fitness()
                generation_alive = True

        # draw 
        screen.blit(track, (0, 0))
        for car in cars:
            if car.alive:
                car.draw(screen)

        generation_text = font.render(f'GENERATION: {generation}', True, (0, 0, 255))
        screen.blit(generation_text, (10, 10))        
        pygame.display.flip()

        if not generation_alive:
            running = False

        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    global generation
    generation = -1
    
    config_path = "config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    population.run(run_generation, 300)