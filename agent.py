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
    
    listscore = []
    for i in range(len(list)):
        node1 = list[i][0]
        node2 = list[i][1]
        listscore.append(node1.score - node2.score)
    
    stuck = True
    for score in listscore:
        if score >0:
            stuck = False
            break

    if stuck:
        for key in coups:
            if key.score == 4:
                list=[]
                for value in coups[key]:
                    list.append(value)
                move = (key, random.choice(list))
                break
    else:
        move = list[listscore.index(max(listscore))]
    b = game.agent.play(move[0],move[1],game)
    return b