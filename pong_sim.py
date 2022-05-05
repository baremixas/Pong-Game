import pygame
from sys import exit
import random

pygame.init()

screen_res = (800, 600)
screen = pygame.display.set_mode(screen_res)

class Player():
    def __init__(self,x_pos,y_pos,speed):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.move = 0
        self.length = 140
        self.thick = 10
        self.rect = pygame.Rect(self.x_pos-self.thick, self.y_pos-self.length/2, self.thick, self.length)
    def movement_limit(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_res[1]:
            self.rect.bottom = screen_res[1]
    def reset(self):
        self.rect.topleft = (self.x_pos-self.thick, self.y_pos-self.length/2)
    def update(self):
        # self.rect.y += self.move
        # self.movement_limit()
        pygame.draw.rect(screen, 'White', self.rect)

class Opponent():
    def __init__(self,x_pos,y_pos,speed):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.move = 0
        self.length = 140
        self.thick = 10
        self.rect = pygame.Rect(self.x_pos, self.y_pos-self.length/2, self.thick, self.length)
    def movement_limit(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_res[1]:
            self.rect.bottom = screen_res[1]
    def reset(self):
        self.rect.topleft = (self.x_pos, self.y_pos-self.length/2)
    def update(self):
        # self.movement_limit()
        pygame.draw.rect(screen, 'White', self.rect)

class Ball():
    def __init__(self,x_pos,y_pos,x_speed,y_speed,player,opponent):
        super().__init__()
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
        self.rect = pygame.Rect(x_pos-self.diameter/2, y_pos-self.diameter/2, self.diameter, self.diameter)
    def collisions(self):
        # bouncing from walls
        if self.y_speed < 0 and self.rect.top <= 0:
            self.y_speed *= -1
        if self.y_speed > 0 and self.rect.bottom >= screen_res[1]:
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
                if self.rect.x <= self.opponent.rect.x + self.opponent.thick:
                    # invert x speed
                    self.x_speed *= -1
                    # adjust y speed
                    self.y_speed = -1 * (self.opponent.rect.y + self.opponent.length / 2 - (self.rect.y + self.diameter / 2)) / (self.opponent.length / 2 / self.y_speed_def)
                    # counting opponent's paddle hits
                    self.opponent_hits += 1

        # scoring points
        if self.rect.right >= screen_res[0]:
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
        self.rect.center = (screen_res[0] / 2, screen_res[1] / 2)
        # randomizing ball direction
        self.x_speed = self.x_speed_def * random.choice([-1, 1])
        self.y_speed = self.y_speed_def * random.choice([-1, 1])
    def update(self):
        # if self.game_state == True:
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.collisions()

class GameInfo:
    def __init__(self, opponent_hits, player_hits, opponent_score, player_score):
        self.opponent_hits = opponent_hits
        self.player_hits = player_hits
        self.opponent_score = opponent_score
        self.player_score = player_score

class Game:
    def __init__(self, screen, screen_res):
        self.screen = screen
        self.screen_res = screen_res

        self.background_color = 'Black'
        self.font_size = 80
        self.font = pygame.font.Font(None, self.font_size)

        # initialize score texts and boxes
        self.player_points = self.font.render('0', False, 'White')
        self.player_points_box = self.player_points.get_rect(midtop = (self.screen_res[0] / 4, 20))
        self.opponent_points = self.font.render('0', False, 'White')
        self.opponent_points_box = self.opponent_points.get_rect(midtop = (self.screen_res[0] * 3 / 4, 20))
        self.hits_sum = self.font.render('0', False, 'White')
        self.hits_sum_box = self.hits_sum.get_rect(midtop = (self.screen_res[0] / 2, 20))

        # objects
        self.player = Player(self.screen_res[0] - 20, self.screen_res[1] / 2, 5)
        self.opponent = Opponent(20, self.screen_res[1] / 2, 5)

        self.x_speed = 5
        self.y_speed = 5
        self.ball = Ball(self.screen_res[0] / 2, self.screen_res[1] / 2, self.x_speed, self.y_speed, self.player, self.opponent)
    def display_score(self):
        # drawing score
        self.player_points = self.font.render(f'{self.ball.player_points}', False, 'White')
        self.opponent_points = self.font.render(f'{self.ball.opponent_points}', False, 'White')
        self.screen.blit(self.player_points, self.player_points_box)
        self.screen.blit(self.opponent_points, self.opponent_points_box)
    def display_hits(self):
        self.hits_sum = self.font.render(f'{self.ball.player_hits + self.ball.opponent_hits}', False, 'White')
        self.screen.blit(self.hits_sum, self.hits_sum_box)
    def display(self, score=True, hits=True):
        self.screen.fill(self.background_color)
        pygame.draw.aaline(self.screen, 'White', (self.screen_res[0] / 2, 0), (self.screen_res[0] / 2, self.screen_res[1]))

        if score == True:
            self.display_score()
        if hits == True:
            self.display_hits()

        self.player.update()
        self.opponent.update()
        pygame.draw.ellipse(self.screen, 'White', self.ball.rect)
    def move(self, left=False, up=True):
        # moving left (opponent's) paddle
        if left == True:
            if up == True:
                # restriction from top
                if self.opponent.rect.y - self.opponent.speed < 0:
                    return False
                else:
                    self.opponent.rect.y -= self.opponent.speed
            if up == False:
                # restriction from bottom
                if self.opponent.rect.y + self.opponent.length > self.screen_res[1]:
                    return False
                else:
                    self.opponent.rect.y += self.opponent.speed

        # moving right (player's) paddle
        else:
            if up == True:
                if self.player.rect.y - self.player.speed < 0:
                    return False
                else:
                    self.player.rect.y -= self.player.speed
            else:
                if self.player.rect.y + self.player.length > self.screen_res[1]:
                    return False
                else:
                    self.player.rect.y += self.player.speed

        return True
    def loop(self):
        self.ball.update()

        game_info = GameInfo(self.ball.opponent_hits,self.ball.player_hits,self.ball.opponent_points,self.ball.player_points)

        return game_info
    def reset(self):
        self.ball.reset()
        self.opponent.reset()
        self.player.reset()
        self.ball.player_points = 0
        self.ball.opponent_points = 0
