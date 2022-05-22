import pygame
import os
import neat
import pickle
from entities import Player, Ball

pygame.init()
clock = pygame.time.Clock()


class Game:
    def __init__(self, screen, screen_res):
        self.initialize(screen, screen_res)

    def initialize(self, screen, screen_res):
        self.SCREEN = screen
        self.SCREEN_RES = screen_res

        self.ENTITY_COLOR = 'White'
        self.BACKGROUND_COLOR = 'Black'
        self.FONT_SIZE = 80
        self.font = pygame.font.Font(None, self.FONT_SIZE)

        self.player_points = 0
        self.opponent_points = 0
        self.game_state = True

        # Initialize score texts and boxes
        self.player_points_text = self.font.render('0', False, 'White')
        self.player_points_box = self.player_points_text.get_rect(midtop = (self.SCREEN_RES[0] / 4, 20))
        self.opponent_points_text = self.font.render('0', False, 'White')
        self.opponent_points_box = self.opponent_points_text.get_rect(midtop = (self.SCREEN_RES[0] * 3 / 4, 20))
        self.hits_sum = self.font.render('0', False, 'White')
        self.hits_sum_box = self.hits_sum.get_rect(midtop = (self.SCREEN_RES[0] / 2, 20))

        self.PLAYER_LENGTH = 140
        self.PLAYER_THICKNESS = 10
        self.PLAYER_SPEED = 5
        self.OPPONENT_LENGTH = 140
        self.OPPONENT_THICKNESS = 10
        self.OPPONENT_SPEED = 5
        self.WALL_OFFSET = 20

        self.player = Player(self.WALL_OFFSET, self.PLAYER_SPEED, False,
                             self.SCREEN_RES, self.SCREEN, self.PLAYER_LENGTH, self.PLAYER_THICKNESS)
        self.opponent = Player(self.WALL_OFFSET, self.OPPONENT_SPEED, True,
                               self.SCREEN_RES, self.SCREEN, self.OPPONENT_LENGTH, self.OPPONENT_THICKNESS)

        self.BALL_DIAMETER = 30
        self.BALL_X_SPEED = 5
        self.BALL_Y_SPEED = 5

        self.ball = Ball(self.BALL_X_SPEED, self.BALL_Y_SPEED, self.player, self.opponent,
                         self.SCREEN_RES, self.SCREEN, self.BALL_DIAMETER)

    def display_score(self):
        self.player_points_text = self.font.render(f'{self.player_points}', False, 'White')
        self.opponent_points_text = self.font.render(f'{self.opponent_points}', False, 'White')
        self.SCREEN.blit(self.player_points_text, self.player_points_box)
        self.SCREEN.blit(self.opponent_points_text, self.opponent_points_box)

    def display_hits(self):
        self.hits_sum = self.font.render(f'{self.ball.player_hits + self.ball.opponent_hits}', False, 'White')
        self.SCREEN.blit(self.hits_sum, self.hits_sum_box)

    def display_game(self, score=True, hits=False):
        self.SCREEN.fill(self.BACKGROUND_COLOR)
        pygame.draw.aaline(self.SCREEN, 'White', (self.SCREEN_RES[0]/2, 0), (self.SCREEN_RES[0]/2, self.SCREEN_RES[1]))

        if score:
            self.display_score()
        if hits:
            self.display_hits()

        # Drawing paddles and ball
        pygame.draw.rect(self.SCREEN, self.ENTITY_COLOR, self.player.rect)
        pygame.draw.rect(self.SCREEN, self.ENTITY_COLOR, self.opponent.rect)
        pygame.draw.ellipse(self.SCREEN, self.ENTITY_COLOR, self.ball.rect)

    @staticmethod
    def move(paddle, up):
        paddle.movement(up)

    def score_points(self):
        if self.ball.rect.right >= self.SCREEN_RES[0]:
            self.player_points += 1
            self.reset_entities()
            self.game_state = True
        if self.ball.rect.left <= 0:
            self.opponent_points += 1
            self.reset_entities()
            self.game_state = True

    def game_loop(self):
        self.ball.update()
        self.score_points()

    def reset_entities(self):
        self.ball.reset()
        self.player.reset()
        self.opponent.reset()

    def reset_game(self):
        self.reset_entities()
        self.player_points = 0
        self.opponent_points = 0

    @staticmethod
    def load_ai():
        # Import NEAT configuration file
        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, 'config.txt')
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

        best = pickle.load(open("best.pickle", 'rb'))

        return neat.nn.FeedForwardNetwork.create(best, config)

    def play(self, play_ai):
        '''Function used for playing Pong game. A bool input indicates if the game is versus AI loaded from file
        or versus second player.
        '''

        if play_ai:
            network = self.load_ai()

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()

            if self.game_state:
                if keys[pygame.K_SPACE]:
                    self.game_state = False
            else:
                if keys[pygame.K_UP]:
                    self.move(self.player, True)
                if keys[pygame.K_DOWN]:
                    self.move(self.player, False)

                if play_ai:
                    # AI controls second paddle
                    output = network.activate((self.opponent.rect.y, self.ball.rect.y,
                                               abs(self.opponent.rect.x - self.ball.rect.x)))
                    decision = output.index(max(output))
                    if decision == 0:
                        pass
                    elif decision == 1:
                        self.move(self.opponent, True)
                    elif decision == 2:
                        self.move(self.opponent, False)
                else:
                    # Second player controls second paddle
                    if keys[pygame.K_w]:
                        self.move(self.opponent, True)
                    if keys[pygame.K_s]:
                        self.move(self.opponent, False)

                self.game_loop()

            self.display_game(score=True, hits=True)
            pygame.display.update()

        pygame.quit()
