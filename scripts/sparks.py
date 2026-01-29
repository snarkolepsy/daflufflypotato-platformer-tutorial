import math

import pygame

class Spark:
    def __init__(self, position, angle, speed):
        """Initialize the Spark object

        :param position: List of x and y coordinates
        :param angle: The angle of attack
        :param speed: The speed of the animation
        """
        self.position = list(position)
        self.angle = angle
        self.speed = speed

    def update(self):
        """Updating the Spark object's position based on angle as speed decreases

        :return: True when the speed is zero (i.e. stopped)
        """
        self.position[0] += math.cos(self.angle) * self.speed
        self.position[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)
        return not self.speed

    def render(self, surface, offset=(0, 0)):
        """

        :return:
        """
        render_points = [
            (self.position[0] + math.cos(self.angle) * self.speed * 3 - offset[0], self.position[1] + math.sin(self.angle) * self.speed * 3 - offset[1]), # Angle as is
            (self.position[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[0], self.position[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[1]), # 90 degree
            (self.position[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0], self.position[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1]), # 180 degree
            (self.position[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[0], self.position[1] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[1]), # Technically 270 degree
        ]
        pygame.draw.polygon(surface, (255, 255, 255), render_points)