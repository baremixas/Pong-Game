import pygame
import random

pygame.init()


class Player():
    def __init__(self, wall_offset, speed, left, screen_res, screen, length, thickness):
        self.initialize(wall_offset, speed, left, screen_res, screen, length, thickness)

    def initialize(self, wall_offset, speed, left, screen_res, screen, length, thickness):
        '''Used to initialize all parameters of the object'''

        self.speed = speed
        self.wall_offset = wall_offset
        self.left = left
        self.screen_res = screen_res
        self.screen = screen
        self.y_pos = screen_res[1]/2

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


class Ball():
    def __init__(self, x_speed, y_speed, player, opponent, screen_res, screen, diameter):
        self.initialize(x_speed, y_speed, player, opponent, screen_res, screen, diameter)

    def initialize(self, x_speed, y_speed, player, opponent, screen_res, screen, diameter):
        '''Used to initialize all parameters of the ball'''

        self.x_speed_start = x_speed
        self.y_speed_start = y_speed
        self.x_speed = self.x_speed_start * random.choice([-1, 1])
        self.y_speed = self.y_speed_start * random.choice([-1, 1])

        self.player = player
        self.opponent = opponent
        self.player_hits = 0
        self.opponent_hits = 0
        self.screen_res = screen_res
        self.screen = screen

        self.diameter = diameter
        self.rect = pygame.Rect(self.screen_res[0]/2 - self.diameter/2, self.screen_res[1]/2 - self.diameter/2,
                                self.diameter, self.diameter)

    def adjust_y_speed(self, paddle):
        self.y_speed = -1 * (paddle.rect.y + paddle.length/2 -
                             (self.rect.y + self.diameter/2)) / (paddle.length/2/self.y_speed_start)

    def player_collision(self):
        # Checking for side collisionns
        if self.rect.y + self.diameter >= self.player.rect.y \
                and self.rect.y <= self.player.rect.y + self.player.length:
            if self.rect.x + self.diameter >= self.player.rect.x:
                self.x_speed *= -1
                self.adjust_y_speed(self.player)
                self.player_hits += 1

    def opponent_collision(self):
        # Checking for side collisions
        if self.rect.y + self.diameter >= self.opponent.rect.y \
                and self.rect.y <= self.opponent.rect.y + self.opponent.length:
            if self.rect.x <= self.opponent.rect.x + self.opponent.thickness:
                self.x_speed *= -1
                self.adjust_y_speed(self.opponent)
                self.opponent_hits += 1

    def collisions(self):
        # Bouncing from walls
        if self.y_speed < 0 and self.rect.top <= 0:
            self.y_speed *= -1
        if self.y_speed > 0 and self.rect.bottom >= self.screen_res[1]:
            self.y_speed *= -1

        # Checking which way the ball is moving and checking collisions with paddles
        if self.x_speed > 0:
            self.player_collision()
        if self.x_speed < 0:
            self.opponent_collision()

    def reset(self):
        self.player_hits = 0
        self.opponent_hits = 0

        # Centering the ball
        self.rect.center = (self.screen_res[0]/2, self.screen_res[1]/2)

        # Randomizing ball direction
        self.x_speed = self.x_speed_start * random.choice([-1, 1])
        self.y_speed = self.y_speed_start * random.choice([-1, 1])

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.collisions()

