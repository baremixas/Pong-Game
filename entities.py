import pygame
from sys import exit
import random

pygame.init()


class Player():
    def __init__(self, wall_offset, y_pos, speed, left, screen_res, screen, length, thickness):
        self.initialize(wall_offset, y_pos, speed, left, screen_res, screen, length, thickness)

    def initialize(self, wall_offset, y_pos, speed, left, screen_res, screen, length, thickness):
        '''A function used to initialize all parameters of the object'''

        self.y_pos = y_pos
        self.speed = speed
        self.wall_offset = wall_offset
        self.left = left
        self.screen_res = screen_res
        self.screen = screen

        # Size of the paddle
        self.length = length
        self.thickness = thickness

        # Setting position according to left/right placement
        if self.left:
            self.rect = pygame.Rect(self.wall_offset, self.y_pos - self.length / 2, self.thickness, self.length)
        else:
            self.rect = pygame.Rect(self.screen_res[0] - self.wall_offset - self.thickness,
                                    self.y_pos - self.length / 2, self.thickness, self.length)

    def movement(self, up):
        if up:
            self.movement_up()
        else:
            self.movement_down()

    def movement_up(self):
        if self.rect.y - self.speed <= 0:
            self.rect.top = 0
        else:
            self.rect.y -= self.speed

    def movement_down(self):
        if self.rect.y + self.length + self.speed >= self.screen_res[1]:
            self.rect.bottom = self.screen_res[1]
        else:
            self.rect.y += self.speed

    def reset(self):
        if self.left:
            self.rect.topleft = (self.wall_offset, self.y_pos - self.length/2)
        else:
            self.rect.topleft = (self.screen_res[0] - self.wall_offset - self.thickness, self.y_pos - self.length / 2)

    def update(self):
        pygame.draw.rect(self.screen, 'White', self.rect)


class Ball():
    def __init__(self, x_pos, y_pos, x_speed, y_speed, player, opponent, screen_res, screen):
        self.x_speed_def = x_speed
        self.y_speed_def = y_speed
        self.x_speed = self.x_speed_def * random.choice([-1, 1])
        self.y_speed = self.y_speed_def * random.choice([-1, 1])
        self.game_state = False
        self.player = player
        self.opponent = opponent
        self.player_points = 0
        self.opponent_points = 0
        self.player_hits = 0
        self.opponent_hits = 0
        self.diameter = 30
        self.screen_res = screen_res
        self.screen = screen

        self.rect = pygame.Rect(x_pos-self.diameter/2, y_pos-self.diameter/2, self.diameter, self.diameter)
    def collisions(self):
        # bouncing from walls
        if self.y_speed < 0 and self.rect.top <= 0:
            self.y_speed *= -1
        if self.y_speed > 0 and self.rect.bottom >= self.screen_res[1]:
            self.y_speed *= -1

        # bouncing from players
        # checking which way the ball is moving
        if self.x_speed > 0:
            # checking for side collision
            if self.rect.y + self.diameter >= self.player.rect.y and self.rect.y <= self.player.rect.y + self.player.length:
                if self.rect.x + self.diameter >= self.player.rect.x:
                    # invert x speed
                    self.x_speed *= -1
                    # adjust y speed
                    self.y_speed = -1 * (self.player.rect.y + self.player.length / 2 - (self.rect.y + self.diameter / 2)) / (self.player.length / 2 / self.y_speed_def)
                    # counting player's paddle hits
                    self.player_hits += 1
        if self.x_speed < 0:
            # checking for side collision
            if self.rect.y + self.diameter >= self.opponent.rect.y and self.rect.y <= self.opponent.rect.y + self.opponent.length:
                if self.rect.x <= self.opponent.rect.x + self.opponent.thickness:
                    # invert x speed
                    self.x_speed *= -1
                    # adjust y speed
                    self.y_speed = -1 * (self.opponent.rect.y + self.opponent.length / 2 - (self.rect.y + self.diameter / 2)) / (self.opponent.length / 2 / self.y_speed_def)
                    # counting opponent's paddle hits
                    self.opponent_hits += 1

        # scoring points
        if self.rect.right >= self.screen_res[0]:
            self.player_points += 1
            self.reset()
        if self.rect.left <= 0:
            self.opponent_points += 1
            self.reset()
    def reset(self):
        # self.game_state = False
        # reseting counters
        self.player_hits = 0
        self.opponent_hits = 0
        # centering the ball
        self.rect.center = (self.screen_res[0] / 2, self.screen_res[1] / 2)
        # randomizing ball direction
        self.x_speed = self.x_speed_def * random.choice([-1, 1])
        self.y_speed = self.y_speed_def * random.choice([-1, 1])
    def update(self):
        # if self.game_state == True:
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.collisions()

