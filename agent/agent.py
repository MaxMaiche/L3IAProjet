import Game.game as Game
import Game.pygameGUI
import random

def randomAgent(game:Game):
    coups = game.agent.getCoups()
    node = coups.keys().random().choice()
    node2 = coups[node].random().choice()
    game.agent.play(node,node2)