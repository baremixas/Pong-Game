import pygame
from game import Game
import os
import neat
import pickle

pygame.init()
clock = pygame.time.Clock()

class PongGame:
    def __init__(self, screen, screen_res):
        self.game = Game(screen,screen_res)
        self.player = self.game.player
        self.opponent = self.game.opponent
        self.ball = self.game.ball

    # testing the game with trained ai
    def play_ai(self, genome, config):
        network = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            # player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move(left=False, up=True)
            if keys[pygame.K_s]:
                self.game.move(left=False, up=False)

            # AI's controls
            output = network.activate((self.opponent.rect.y, self.ball.rect.y, abs(self.opponent.rect.x - self.ball.rect.x)))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.move(left=True, up=True)
            else:
                self.game.move(left=True, up=False)

            game_info = self.game.loop()
            self.game.display(True, True)
            pygame.display.update()
        pygame.quit()

    # calculating fitness of genome
    def calculate_fitness(self, genome1, genome2, game_info):
        # genome's fitness is amount of hits of its paddle
        genome1.fitness += game_info.opponent_hits - game_info.player_hits
        genome2.fitness += game_info.player_hits - game_info.opponent_hits

    # training the ai
    def train_ai(self, genome1, genome2, config):
        # defining networks
        network1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        network2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # setting outputs for network 1, which is moving opponent's paddle
            output1 = network1.activate((self.opponent.rect.y, self.ball.rect.y, abs(self.opponent.rect.x - self.ball.rect.x), self.player.rect.y))
            # taking the max output value as decision maker
            decision1 = output1.index(max(output1))
            # assigning actions to decision value
            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move(left=True, up=True)
            else:
                self.game.move(left=True, up=False)

            output2 = network2.activate((self.player.rect.y, self.ball.rect.y, abs(self.player.rect.x - self.ball.rect.x), self.opponent.rect.y))
            decision2 = output2.index(max(output2))

            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move(left=False, up=True)
            else:
                self.game.move(left=False, up=False)

            game_info = self.game.loop()
            # displaying images on screen
            self.game.display(True,True)
            pygame.display.update()

            # ending session if any paddle misses ball or the game is too long so the learning goes faster
            if game_info.opponent_hits + game_info.player_hits >= 50:
                self.ball.player_points += 1
                self.ball.opponent_points += 1
                self.ball.reset()
            if game_info.player_score + game_info.opponent_score >= 10:
                self.calculate_fitness(genome1, genome2, game_info)
                break

# testing genomes and checking their fitness
def eval_genomes(genomes, config):
    screen_res = (800,600)
    screen = pygame.display.set_mode(screen_res)

    # running genome1 against every other genome one time
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break

        genome1.fitness = 0

        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(screen,screen_res)
            game.train_ai(genome1, genome2, config)

# running neat through declared amount of generations
def run_neat(config):
    # setting population for algorithm
    population = neat.Population(config)
    # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-44')
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    # checkpointing after each generation
    population.add_reporter(neat.Checkpointer(1))

    # calculating fitness of each genome in generation
    best = population.run(eval_genomes, 50)
    # saving best genome object
    with open("best.pickle", 'wb') as f:
        pickle.dump(best, f)

# testing game with best genome
def play_ai(config):
    # opening saved best genome
    with open("best.pickle", 'rb') as ai:
        best = pickle.load(ai)

    # setting up the window for game
    screen_res = (800,600)
    screen = pygame.display.set_mode(screen_res)

    # starting the game
    game = PongGame(screen,screen_res)
    game.play_ai(best, config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    run_neat(config)
    # play_ai(config)
