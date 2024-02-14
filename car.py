import math
import pygame

CAR_LENGHT = 45
CAR_WIDTH = 20
COLOR = 'red'

class Car:
    def __init__(self, init_x, init_y, angle=-90):
        self.x = init_x
        self.y = init_y
        self.speed = 0
        self.angle = angle

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
            rotated_points.append((rotated_x, rotated_y))

        return rotated_points