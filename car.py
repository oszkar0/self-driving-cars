import math
import pygame

CAR_LENGHT = 45
CAR_WIDTH = 20
COLOR = 'red'
MAX_SPEED = 200
GAS_ACCELERATION = 250
FRICTION_DECELERATION = 5
ANGLE_INCREASE = 30

class Car:
    def __init__(self, init_x, init_y, angle=-90, ai=False):
        self.x = init_x
        self.y = init_y
        self.speed = 0
        self.angle = angle
        self.ai = ai
        self.alive = True

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


    def get_neaural_network_controls(self):
        pass

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

        ## turn controls
        if self.speed != 0:
            flip = 1 if self.speed > 0 else -1
            if left:
                self.angle += dt * ANGLE_INCREASE * flip
            if right:
                self.angle -= dt * ANGLE_INCREASE * flip

        ## update position
        self.x += -self.speed * dt * math.sin(math.radians(self.angle))
        self.y += -self.speed * dt * math.cos(math.radians(self.angle))

        ## check for collision
        ## if any of the corners of car rect is on collision color then we have collision
        car_points_cords = self.calculate_rotated_car_points()

        if any(track.get_at(point) == collision_color for point in car_points_cords):
            self.alive = False
        




    def draw(self, screen):
        car_points = self.calculate_rotated_car_points()
        pygame.draw.polygon(screen, COLOR, car_points)

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



class Radar():
    def __init__(self, ray_count, ray_spread, ray_length):
        self.ray_count = ray_count
        self.ray_length = ray_length
        self.ray_spread = ray_spread

        self.rays = []
        self.ray_colision_points = []
        self.ray_colision_points_dst = []