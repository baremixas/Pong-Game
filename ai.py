import pygame
import os
import neat
import pickle
from game import Game

pygame.init()
clock = pygame.time.Clock()


class AI:
    def __init__(self, screen, screen_res):
        '''The class is used for training the AI in Pong game.'''

        self.screen = screen
        self.screen_res = screen_res

    @staticmethod
    def get_config():
        # Import NEAT configuration file
        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, 'config.txt')

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

        return config

    def eval_genomes(self, genomes, config):
        '''This is function responsible for calling the game loop and calculating fitness of each genome.'''

        config = self.get_config()

        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            genome.fitness = 0
            self.game = Game(self.screen, self.screen_res)
            self.game_loop(network, config)
            genome.fitness += self.game.ball.opponent_hits

    def train(self):
        '''In this function we create our population and run the NEAT algorithm with our objective function and
        save the best genome to the file, so we can play against it later.
        '''

        config = self.get_config()
        population = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        population.add_reporter(neat.Checkpointer(1))

        best = population.run(self.eval_genomes, 50)  # Getting the best genome after number of generations (50)

        pickle.dump(best, open("best.pickle", 'wb'))

    def game_loop(self, network, config):
        '''This is the function where the game takes place.

        The opponent for AI was manually programmed to always keep the ball on it's body length.
        The game lasts to the first point on whatever side.
        '''
        
        run = True
        while run:
            clock.tick() # Set FPS (higher value = faster simulation), empty to no max restriction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # AI's controls
            output = network.activate((self.game.opponent.rect.y, self.game.ball.rect.y,
                                       abs(self.game.opponent.rect.x - self.game.ball.rect.x)))
            decision = output.index(max(output))
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move(self.game.opponent, True)
            elif decision == 2:
                self.game.move(self.game.opponent, False)

            # Opponent for AI
            if self.game.ball.rect.y >= self.game.player.rect.y + self.game.PLAYER_LENGTH:
                print("TRUE")
                self.game.move(self.game.player, False)
            if self.game.ball.rect.y + self.game.BALL_DIAMETER <= self.game.player.rect.y:
                print('FALSE')
                self.game.move(self.game.player, True)

            self.game.game_loop()
            self.game.display_game(score=True, hits=True)
            pygame.display.update()

            if self.game.opponent_points != 0 or self.game.player_points != 0:
                break
