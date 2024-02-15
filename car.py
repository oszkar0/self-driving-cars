import math
import pygame
import time 
from network import MutableNeuralNetwork, FullyConnectedLayer
import numpy as np

CAR_LENGHT = 45
CAR_WIDTH = 20
COLOR = 'red'
MAX_SPEED = 200
GAS_ACCELERATION = 250
FRICTION_DECELERATION = 5
ANGLE_INCREASE = 30

class Car:
    def __init__(self, init_x, init_y, angle=-90, ray_count=5, ray_spread=math.pi/2, ray_length=100, ai=False):
        self.x = init_x
        self.y = init_y
        self.speed = 0
        self.angle = angle
        self.ai = ai
        self.alive = True
        self.radar = Radar(ray_count, ray_spread, ray_length)
        self.distance = 0;
        self.birth_time = time.time()
        self.time_alive = 0;
        self.car_info = np.ones(ray_count + 1).reshape(1, -1)
        self.last_check_time = time.time()
        self.last_distance = 0
    
        if self.ai:
            self.brain = MutableNeuralNetwork([
                FullyConnectedLayer(ray_count + 1, ray_count + 1), # input = sensors + speed
                FullyConnectedLayer(ray_count + 1, ray_count + 1),
                FullyConnectedLayer(ray_count + 1, 2) ## output = rear/forward + left/right
            ])

    def get_keyboard_controls(self):
        keys = pygame.key.get_pressed()
        left, right, forward, rear = False, False, False, False

        if keys[pygame.K_w]:
            forward = True
        if keys[pygame.K_s]:
            rear = True
        if keys[pygame.K_a]:
            left = True
        if keys[pygame.K_d]:
            right = True

        return left, right, forward, rear


    def get_neural_network_controls(self):
        left, right, forward, rear = False, False, False, False
        self.car_info[:, :-1] = 1 - self.car_info[:, :-1] / self.radar.ray_length
        self.car_info[:, -1] = self.car_info[:, -1] / MAX_SPEED
        steering = self.brain.predict(self.car_info)

        if steering[0, 0] >= 0:
            forward = True
        else: 
            rear = True

        if steering[0, 1] >= 0:
            right = True
        else:
            left = True

        return left, right, forward, rear
        

    def update(self, dt, track, collision_color):
        ## get controls
        if self.ai:
            left, right, forward, rear = self.get_neural_network_controls()
        else: 
            left, right, forward, rear = self.get_keyboard_controls()

        ## speed controls
        if forward:
            self.speed += dt * GAS_ACCELERATION
        if rear:
            self.speed -= dt * GAS_ACCELERATION

        if abs(self.speed) < dt * FRICTION_DECELERATION:
            self.speed = 0
        elif self.speed > 0:
            self.speed -= dt * FRICTION_DECELERATION
        elif self.speed < 0:
            self.speed += dt * FRICTION_DECELERATION

        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED
        if self.speed < -MAX_SPEED / 3:
            self.speed = -MAX_SPEED / 3

        flip = 1 if self.speed > 0 else -1

        ## turn controls
        if self.speed != 0:
            if left:
                self.angle += dt * ANGLE_INCREASE * flip
            if right:
                self.angle -= dt * ANGLE_INCREASE * flip

        ## update position
        new_x = self.x + -self.speed * dt * math.sin(math.radians(self.angle))
        new_y = self.y - self.speed * dt * math.cos(math.radians(self.angle))

        ## new way of calculating distance ensures cars will be driving forward
        self.distance += flip * math.sqrt((new_x - self.x)**2 + (new_y - self.y)**2)

        self.x = new_x
        self.y = new_y 
        
        ## if car keeps driving back and forward in a loop we have to 'kill' him manully
        ## since it might never die
        time_elapsed_since_last_check = time.time() - self.last_check_time

        # Check if two seconds have elapsed since the last check
        if time_elapsed_since_last_check >= 2:
            if abs(self.last_distance - self.distance) < 20:
                self.alive = False

            self.last_check_time = time.time()
            self.last_distance = self.distance

        ## check for collision
        ## if any of the corners of car rect is on collision color then we have collision
        car_points_cords = self.calculate_rotated_car_points()

        if any(track.get_at(point) == collision_color for point in car_points_cords):
            self.time_alive = time.time() - self.birth_time
            self.alive = False
        
        ##check radars
        radar_readings = self.radar.check_radar(self.x, self.y, self.angle, track, collision_color)
        self.car_info = np.hstack([radar_readings, self.speed]).reshape(1, -1)

    def draw(self, screen):
        car_points = self.calculate_rotated_car_points()
        pygame.draw.polygon(screen, COLOR, car_points)
        self.radar.draw(screen)

    def calculate_rotated_car_points(self):
        angle_rad = math.radians(self.angle)
        ## calculate unrotated points
        x_left = - CAR_WIDTH // 2
        x_right = CAR_WIDTH // 2
        y_top = - CAR_LENGHT // 2
        y_bottom = CAR_LENGHT // 2

        points = [(x_left, y_top), (x_right, y_top), (x_right, y_bottom), (x_left, y_bottom)]

        ## rotate each point around the car's center
        rotated_points = []
        for point in points:
            rotated_x = point[0] * math.cos(angle_rad) - point[1] * math.sin(angle_rad)
            rotated_y = -(point[0] * math.sin(angle_rad) + point[1] * math.cos(angle_rad))

            ## translate rotated points
            rotated_x += self.x
            rotated_y += self.y
            rotated_points.append((int(rotated_x), int(rotated_y)))

        return rotated_points
    
    def get_fitness(self):
        ## we reward cars for driving long distances
        return self.distance



class Radar():
    def __init__(self, ray_count, ray_spread, ray_length):
        self.ray_count = ray_count
        self.ray_length = ray_length
        self.ray_spread = ray_spread

        self.ray_cords = []
        self.ray_collision_points = []
        self.ray_collision_points_distances = []

    def check_radar(self, car_x, car_y, angle, track, collision_color):
        self.ray_cords = []
        self.ray_collision_points = []
        self.ray_collision_points_distances = []

        angle0 = self.ray_spread / 2
        angle1 = - self.ray_spread / 2
        dangle = self.ray_spread / (self.ray_count - 1)
        
        ## check if ray collides with road bounds
        for i in range(self.ray_count):
            ray_collided = False

            for dist in range(1, self.ray_length + 1):
                ray_end = (
                    int(car_x - math.sin(angle0 - i * dangle + math.radians(angle)) * dist),
                    int(car_y - math.cos(angle0 - i * dangle + math.radians(angle)) * dist)
                )

                if track.get_at(ray_end) == collision_color:
                    self.ray_collision_points.append(ray_end)
                    break

            self.ray_collision_points_distances.append(dist)
            self.ray_cords.append([(car_x, car_y), ray_end])

        return self.ray_collision_points_distances
    
    def draw(self, screen):
        for line in self.ray_cords:
            pygame.draw.line(screen, 'yellow', line[0], line[1], width=2)

        for collision_point in self.ray_collision_points:
            pygame.draw.circle(screen, 'purple', collision_point, 2)
                

        

