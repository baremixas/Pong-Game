# NEAT-Pong
 
The game was created in Python with use of PyGame and NEAT algorithm and was made to learn and practice basic programming skills fully by me.

## Table of contents
* [General info](#general-info)
* [Future](#future)
* [Screens](#screens)
* [License](#license)

## General info

The program is a classic game of Pong. Two players, each with a paddle, try to hit the ball to score points. The program is using NeuroEvolution of Augmenting Topologies to train the AI, so that user can play by himself.

For the moment, in order to play a game with AI, you need to make changes in code:
- uncomment the "play_ai" function,
- comment "run_neat" function.

The training consist of genome playing a game versus each other genome in the generation.
For now the game lasts 10 points (or more). After each game we update each genome's fitness by adding difference in scores of genomes.
Example:
Game finishes with the score 7:3. Fitness of genome1 is extended by 4 (7 - 3 = 4), while fitness of genome2 is lowered by 4 (3 - 7 = -4).

For informations about NEAT algorithm visit: http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf

## Future

I plan to add things such as:
- main menu to choose from options:
	- teach AI
	- play vs AI
	- play vs another player
- more diversity to the game like pick-up bonuses or increasing speed of the ball
- choosing from AI difficulty

## Screens
<p align="center">
	<img width="40%" src="./Readme_images/game.jpg">
</p>

## License
This project is licensed under the terms of **the MIT license**.
You can check out the full license [here](./LICENSE)
