import game
import random
from copy import deepcopy

def randomAgent(game:game, value):
    coups = dict()
    move = ()
    if value == 1:
        coups = game.joueur1.getCoups()
    else:
        coups = game.joueur2.getCoups()


    list = []
    for key in coups:
        for v in coups[key]:
            list.append((key,v))
    
    move = random.choice(list)
    b=False
    if value == 1:
        b = game.joueur1.play(move[0],move[1],game)
    else:
        b = game.joueur2.play(move[0],move[1],game)

    return b

def greedyAgent(game:game,value):
    coups = dict()
    move = ()
    b = False
 
    coups = game.players[value-1].getCoups()
    list = []
    for key in coups:
        for v in coups[key]:
            list.append((key,v))
        
    listscore = []
    for i in range(len(list)):
        node1 = list[i][0].score
        node2 = list[i][1].score
        listscore.append((node1 - node2, list[i]))
            
    random.shuffle(listscore)    
    if (value == 2): 
        move = max(listscore,key=lambda item:item[0])[1]
    else:
        move = min(listscore,key=lambda item:item[0])[1]

    b = game.players[value-1].play(move[0],move[1],game)
    return b



def minimaxAgent(game:game,value):
    gameCopy = deepcopy(game)
    value=value-1
    coups = gameCopy.players[value].getCoups()
    
    list = []
    for key in coups:
        for v in coups[key]:
            list.append((key,v))
            
    values = []
    for coup in list:
        gameCopy2 = deepcopy(gameCopy)
        depart = gameCopy2.getNode(coup[0].x,coup[0].y)
        arrive = gameCopy2.getNode(coup[1].x,coup[1].y)
        gameCopy2.players[value].play(depart, arrive, gameCopy2)
        values.append((coup,min_value(gameCopy2, value)))
    
    move = max(values,key=lambda item:item[1])[0]
    b= game.players[value].play(move[0],move[1],game)
    return b
    
def min_value(game:game,value):
    if game.isFinished():
        return 1

    value = 1-value
    coups = game.players[value].getCoups()
    
    list = []
    for key in coups:
        for v in coups[key]:
            list.append((key,v))
            
    values = []
    for coup in list:
        gameCopy = deepcopy(game)
        depart = gameCopy.getNode(coup[0].x,coup[0].y)
        arrive = gameCopy.getNode(coup[1].x,coup[1].y)
        gameCopy.players[value].play(depart, arrive, gameCopy)
        values.append(max_value(gameCopy, value))
    return min(values)  


def max_value(game:game,value):
    if game.isFinished():
        return -1
        
    value = 1-value
    coups = game.players[value].getCoups()
    
    list = []
    for key in coups:
        for v in coups[key]:
            list.append((key,v))
            
    values = []
    for coup in list:
        gameCopy = deepcopy(game)
        depart = gameCopy.getNode(coup[0].x,coup[0].y)
        arrive = gameCopy.getNode(coup[1].x,coup[1].y)
        gameCopy.players[value].play(depart, arrive, gameCopy)
        values.append(min_value(gameCopy, value))
    return max(values)