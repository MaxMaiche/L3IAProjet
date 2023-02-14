import game
import random
from copy import deepcopy
from threading import Thread

MAX_VALUE = 1_000_000
MIN_VALUE = -1_000_000


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
    game.lastCoup = move

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
    game.lastCoup = move
    return b




def calculListScore(list):
    listscore = []
    for i in range(len(list)):
        node1 = list[i][0].score
        node2 = list[i][1].score
        listscore.append(node1 - node2)
    return listscore


def alpha_Beta_Agent(game,value,nbProfondeur):

    hash = game.hash()
    if hash in game.memo:
        alpha, beta = game.memo[hash]
    else:
        alpha = MIN_VALUE
        beta = MAX_VALUE

    
    gameCopy = deepcopy(game)
    value=value-1
    coups = gameCopy.players[value].getCoupsListAndScore()

    values = []
    for coup in coups:
        if coup[1]<0:
            break
        coup = coup[0]
        depart = gameCopy.getNode(coup[0].x,coup[0].y)
        arrive = gameCopy.getNode(coup[1].x,coup[1].y)

        gameCopy.players[value].play(depart, arrive, gameCopy)

        #if gameCopy.split():
        #    values.append((coup,max_valueAB_end(gameCopy, value, nbProfondeur-1, alpha, beta)))

        values.append((coup,min_valueAB(gameCopy, 1-value, nbProfondeur-1, alpha, beta, game.memo)))

        gameCopy.players[value].undo(depart, arrive, gameCopy)
    
    move = max(values,key=lambda item:item[1])[0]
    depart = game.getNode(move[0].x,move[0].y)
    arrive = game.getNode(move[1].x,move[1].y)

    b= game.players[value].play(depart,arrive,game)
    return b
    
def min_valueAB(game:game, value, nbProfondeur, alpha, beta, memo):
    if nbProfondeur==0 or game.isFinished():
        return game.eval(1-value)

    hash = game.hash()
    change = False
    if hash in memo:
        alphaMemo, betaMemo = memo[hash]
        if alphaMemo < alpha:
            alpha = alphaMemo
            change = True
        if betaMemo > beta:
            beta = betaMemo
            change = True
    else:
        change = True
    
    if change:
        memo[hash] = (alpha, beta)

    coups = game.players[value].getCoupsListAndScore()

    val = MAX_VALUE
    for coup in coups:
        if coup[1]<0:
            break
        coup = coup[0]
        depart = coup[0]
        arrive = coup[1]

        game.players[value].play(depart, arrive, game)
        val = min(val,max_valueAB(game, 1-value, nbProfondeur-1, alpha, beta, memo))
        game.players[value].undo(depart, arrive, game)

        if val <= alpha:
            return val
        beta = min(beta, val)

    return val  


def max_valueAB(game:game, value, nbProfondeur, alpha, beta, memo):
    if nbProfondeur==0 or game.isFinished():
        return game.eval(value)

    hash = game.hash()
    change = False
    if hash in memo:
        alphaMemo, betaMemo = memo[hash]
        if alphaMemo < alpha:
            alpha = alphaMemo
            change = True
        if betaMemo > beta:
            beta = betaMemo
            change = True
    else:
        change = True
    
    if change:
        memo[hash] = (alpha, beta)

    coups = game.players[value].getCoupsListAndScore()
    val = MIN_VALUE
    for coup in coups:
        if coup[1]<0:
            break
        coup = coup[0]

        depart = coup[0]
        arrive = coup[1]

        game.players[value].play(depart, arrive, game)
        val = max(val,min_valueAB(game, 1-value, nbProfondeur-1, alpha, beta, memo))
        game.players[value].undo(depart, arrive, game)
        
        if val >= beta:
            return val
        alpha = max(alpha, val)

    return val



"""
def max_valueAB_end(game:game,value, nbProfondeur, alpha, beta):
    if nbProfondeur==0 or game.isFinished():
        return game.eval(value)
    
    coups = game.players[value].getCoupsList()
    
    val = MIN_VALUE

    for coup in coups:

        depart = game.getNode(coup[0].x,coup[0].y)
        arrive = game.getNode(coup[1].x,coup[1].y)

        game.players[value].play(depart, arrive, game)
        val = max(val,max_valueAB_end(game, value, nbProfondeur-1, alpha, beta))
        game.players[value].undo(depart, arrive, game)

        if val >= beta:
            return val
        alpha = max(alpha, val)

    return val
"""

def ABThreadAgent(game,value,nbProfondeur):
    value = value-1
    
    coupsEnnemis = game.players[1-value].getCoupsListAndScore()
    threads = []
    for coup in coupsEnnemis:
        coup = coup[0]
        gameCopy = deepcopy(game)
        
        depart = gameCopy.getNode(coup[0].x,coup[0].y)
        arrive = gameCopy.getNode(coup[1].x,coup[1].y)
        game.players[value].play(depart, arrive, game)
        
        x = Thread(target=alpha_Beta_Agent, args=(gameCopy,value,nbProfondeur,coup))
        threads.append((x,coup))
    

    for thread in threads:
        if game.lastMove != None:
            if game.lastMove in game.dictCoupsPredict[value]:
                break
            else:
                if thread[1] == game.lastMove:
                    thread[0].start()
                    thread[0].join()
        else:
            thread[0].start()
            thread[0].join()
    






def testAlpha():
    return

def testBeta():
    return






    """def minimaxAgent(game:game,value, nbProfondeur):
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
        values.append((coup,min_value(gameCopy2, value, nbProfondeur)))
    
    move = max(values,key=lambda item:item[1])[0]
    depart = game.getNode(move[0].x,move[0].y)
    arrive = game.getNode(move[1].x,move[1].y)
    b= game.players[value].play(depart,arrive,game)
    return b
    
def min_value(game:game,value, nbProfondeur):
    if game.isFinished():
        return 1
    
    nbProfondeur-=1
    if nbProfondeur==0:
        return 0
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
        values.append(max_value(gameCopy, value,nbProfondeur))
    return min(values)  


def max_value(game:game,value, nbProfondeur):
    if game.isFinished():
        return -1
    
    nbProfondeur-=1
    if nbProfondeur==0:
        return 0
    
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
        values.append(min_value(gameCopy, value, nbProfondeur))
    return max(values)"""