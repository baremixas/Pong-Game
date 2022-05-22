# NEAT-Pong
 
The game was created in Python with use of PyGame and NEAT algorithm and was made to learn and practice basic programming skills fully by me.

## Table of contents
* [General info](#general-info)
* [Future](#future)
* [Screens](#screens)
* [License](#license)

## General info

The program is a classic game of Pong. Two players, each with a paddle, try to hit the ball to score points. The program is using NeuroEvolution of Augmenting Topologies to train the AI, so that user can play by himself.

The training consist of genome playing a game versus a manually programmed opponent. The game lasts to the first point on either side. The fitness score of genome is increased after each game by amount of times it is able to hit the ball.

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
