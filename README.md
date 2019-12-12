# russianaicup2019

## Intro

Hi! In this repository I have modified the scripts provided by the organizers of the RussianAICup in order to create an AI by using a [NEAT](https://neat-python.readthedocs.io/en/latest/neat_overview.html) (NeuroEvolution of Augmenting Topologies) approach.

## Contest Description

The idea of the contest is to design an AI for a 1v1 platformer-shooting game where your AI will compete against AI's build by the other participants. 
For more information regarding the contest you can visit [their website](https://russianaicup.ru/p/sandbox).

## How to start the game

The game is composed out of two parts:
1. the host   (the actual game)
2. the client (your AI's brain)

In order to open the host, you must run the application which is compatible with your OS.

* aicup2019     for MacOS
* aicup2019.exe for Windows

(there is also a Linux application which I have not yet tried located at ./game/aicup2019-linux.tar)

In order to open the client you must run the main.py script.

For more information regarding the game consult the PDF within ./game/codeside2019-docs-en.pdf.

## How to create a bot

Now, you can either:
* use/modify the baseline strategy provided by the organizers (located at ./strategies/my_strategy.py);
* use my implementation to train your own NEAT bot;
* adapt my implementation to train a DQN/A2C or other fancy RL approach.

## How to use my script

If you go within the ./neat_main.py script, you will see that I've wrapped the code in such way that it will resemble OpenAI's gym library. There are some differences like:
1. In order to render the environment you have to specify the parameter when 'making' the environment;
2. You will need a config.json file (in which you will specify things like the port at which the client to connect, whether to enable/disable the game interface etc.)

(there is already a config file which will always match your bot with a random agent, but if you want to know how to make one, look bellow)

## How to create a config file

In order to create a config file, you need to open the game (look at 'How to start the game') configure the game within the *loading screen* (by clicking the text under **Player 1** or **Player 2**) and click on *save config*.

After that you can even enter the config.json file that you have just created and edit things like ports or wait time etc.

## Additional game settings 

You can see the additional game settings by running:
***./aicup2019 -help*** (or ***aicup.exe -help*** if on Windows)
... in a command line with its root in this repository folder.




