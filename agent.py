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
            node1 = list[i][0]
            node2 = list[i][1]
            listscore.append(node1.score - node2.score)
        
        stuck = True
        for score in listscore:
            if score < 0:
                stuck = False
                break
            
        move = ()
        if stuck:
            for key in coups:
                if key.score <= 12:
                    list=[]
                    for v in coups[key]:
                        list.append(v)
                    move = (key, random.choice(list))
                    break
        else:
            move = list[listscore.index(min(listscore))]
        b = game.joueur1.play(move[0],move[1],game)
    else:
        coups = game.joueur2.getCoups()

        list = []
        for key in coups:
            for v in coups[key]:
                list.append((key,v))
        
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
            
        move = ()
        if stuck:
            for key in coups:
                if key.score >= 4:
                    list=[]
                    for v in coups[key]:
                        list.append(v)
                    move = (key, random.choice(list))
                    break
        else:
            move = list[listscore.index(max(listscore))]
        b = game.joueur2.play(move[0],move[1],game)
    

    return b