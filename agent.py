import game
import pygameGUI
import random

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
    if value == 1:
        coups = game.joueur1.getCoups()
        list = []
        for key in coups:
            for v in coups[key]:
                list.append((key,v))
        
        listscore = []
        for i in range(len(list)):
            node1 = list[i][0].score
            node2 = list[i][1].score
            if node1-node2 == 0:
                listscore.append((-0.5,list[i]))
            else:
                listscore.append((node1 - node2, list[i]))
        
        random.shuffle(listscore)    
        move = min(listscore,key=lambda item:item[0])[1]
        b = game.joueur1.play(move[0],move[1],game)
    else:
        coups = game.joueur2.getCoups()

        list = []
        for key in coups:
            for v in coups[key]:
                list.append((key,v))
        
        listscore = []
        for i in range(len(list)):
            node1 = list[i][0].score
            node2 = list[i][1].score
            if node1-node2 == 0:
                listscore.append((0.5,list[i]))
            else:
                listscore.append((node1 - node2,list[i]))
        
        random.shuffle(listscore) 
        move = max(listscore,key=lambda item:item[0])[1]
        b = game.joueur2.play(move[0],move[1],game)
    

    return b