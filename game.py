import pygame
from sys import exit
from entities import Player, Ball

PLAYER_LENGTH = 140
PLAYER_THICKNESS = 10
OPPONENT_LENGTH = 140
OPPONENT_THICKNESS = 10
WALL_OFFSET = 20


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
        self.player = Player(WALL_OFFSET, self.screen_res[1] / 2, 5, False,
                             screen_res, screen, PLAYER_LENGTH, PLAYER_THICKNESS)
        self.opponent = Player(WALL_OFFSET, self.screen_res[1] / 2, 5, True,
                               screen_res, screen, OPPONENT_LENGTH, OPPONENT_THICKNESS)

        self.x_speed = 5
        self.y_speed = 5
        self.ball = Ball(self.screen_res[0] / 2, self.screen_res[1] / 2, self.x_speed,
                         self.y_speed, self.player, self.opponent, screen_res, screen)

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

        if score:
            self.display_score()

        if hits:
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
