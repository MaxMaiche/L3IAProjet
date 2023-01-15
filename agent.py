import game
import pygameGUI
import random

def randomAgent(game:game):
    coups = game.agent.getCoups()
    list = []
    for key in coups:
        for value in coups[key]:
            list.append((key,value))
    
    move = random.choice(list)
    b = game.agent.play(move[0],move[1],game)
    return b

def greedyAgent(game:game):
    coups = game.agent.getCoups()
    list = []
    for key in coups:
        for value in coups[key]:
            list.append((key,value))
    
    max = list[0]
    for i in range(1,len(list)):
        node1 = list[i][0]
        node2 = list[i][1]
        if node1.score-node2.score > max[0].score-max[1].score:
            max = list[i]
    move = max
    print(move)
    b = game.agent.play(move[0],move[1],game)
    return b