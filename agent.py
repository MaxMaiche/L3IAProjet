import game
import random

def randomAgent(game:game, value):
    coups = dict()
    move = ()
    
    coups = game.players[value-1].getCoups()

    list = []
    for key in coups:
        for v in coups[key]:
            list.append((key,v))
    
    move = random.choice(list)
    b=False

 
    b = game.players[value-1].play(move[0],move[1],game)

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
