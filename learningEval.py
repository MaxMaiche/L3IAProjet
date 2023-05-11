from random import random,uniform,randint,choice,shuffle
import game
from copy import deepcopy

MAX_VALUE = 1_000_000
MIN_VALUE = -1_000_000

def greedyAgentVar(game:game,value):
    """
    Agent Greedy qui retourne le meilleur coup possible pour le joueur value,
    en utilisant une fonction d'évaluation avec des variables
    """
    coups = dict()
    move = ()
    scoreMove = -1000
    b = False
    value = value -1
 
    coups = game.players[value].getCoups()

    list = []
    for key in coups:
        for v in coups[key]:
            list.append((key,v))

    coupsandScore = []
    for coup in list:
        game.players[value].play(coup[0],coup[1],game)
        score = evalVar(game,value)
        game.players[value].undo(coup[0],coup[1],game)
        coupsandScore.append((coup,score))

    shuffle(coupsandScore)
    move = max(coupsandScore,key=lambda item:item[1])[0]
    b = game.players[value].play(move[0],move[1],game)
    return b





def alpha_Beta_Agent_Var(game,value,nbProfondeur):
    """
    Fonction qui retourne le meilleur coup possible pour le joueur value, 
    en utilisant l'algorithme alpha beta et une fonction d'évaluation avec des variables
    """

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

        values.append((coup,max_valueAB(gameCopy, 1-value, nbProfondeur-1, alpha, beta)))

        gameCopy.players[value].undo(depart, arrive, gameCopy)

    shuffle(values)
    move = max(values,key=lambda item:item[1])[0]
    depart = game.getNode(move[0].x,move[0].y)
    arrive = game.getNode(move[1].x,move[1].y)

    b= game.players[value].play(depart,arrive,game)
    return b
    
def min_valueAB(game:game, value, nbProfondeur, alpha, beta):
    """
    Fonction Min de l'algorithme Alpha-Beta mais qui utilise la fonction d'évaluation avec les variables
    game: l'objet game
    value: le joueur qui doit jouer
    nbProfondeur: la profondeur de l'arbre
    alpha: la valeur alpha
    beta: la valeur beta
    """
    if nbProfondeur==0 or game.isFinished():
        return evalVar(game,value)


    coups = game.players[value].getCoupsListAndScore()

    val = MAX_VALUE
    for coup in coups:
        if coup[1]<0:
            break
        coup = coup[0]
        depart = coup[0]
        arrive = coup[1]

        game.players[value].play(depart, arrive, game)
        val = min(val,max_valueAB(game, 1-value, nbProfondeur-1, alpha, beta))
        game.players[value].undo(depart, arrive, game)

        if val <= alpha:
            return val
        beta = min(beta, val)

    return val  


def max_valueAB(game:game, value, nbProfondeur, alpha, beta):
    """
    Fonction Max de l'algorithme Alpha-Beta mais qui utilise la fonction d'évaluation avec les variables
    game: l'objet game
    value: le joueur qui doit jouer
    nbProfondeur: la profondeur de l'arbre
    alpha: la valeur alpha
    beta: la valeur beta
    """
    if nbProfondeur==0 or game.isFinished():
        return evalVar(game,value)


    coups = game.players[value].getCoupsListAndScore()
    val = MIN_VALUE
    for coup in coups:
        if coup[1]<0:
            break
        coup = coup[0]

        depart = coup[0]
        arrive = coup[1]

        game.players[value].play(depart, arrive, game)
        val = max(val,min_valueAB(game, 1-value, nbProfondeur-1, alpha, beta))
        game.players[value].undo(depart, arrive, game)
        
        if val >= beta:
            
            return val
        alpha = max(alpha, val)
    return val


def sd(len, x):
    """
    Calcule la distance au centre pour un noeud
    """
    return ((len//2)- x)**2

def sdMiddle(game,value):
    """
    Calcule la somme des distances au centre pour un joueur
    """
    sd1 = 0
    sd2 = 0

    value = value +1
    
    for y in range(8,0,-1):
        lenLigne = 9-y 
        x=0
        nodeValue = game.getNode(x,y).value
        if nodeValue != 0:
            if nodeValue == value:
                sd1 += sd(lenLigne,y)
            else:
                sd2 += sd(lenLigne,y)
        while y!=8:
            x+=1
            y+=1
            nodeValue = game.getNode(x,y).value
            if nodeValue != 0:
                if nodeValue == value:
                    sd1 += sd(lenLigne,y)
                else:
                    sd2 += sd(lenLigne,y)

        
    for i in range(0,9):
        nodeValue = game.getNode(i,i).value
        if nodeValue != 0:
            lenLigne = 9
            if nodeValue == value:
                sd1 += sd(lenLigne,i)
            else:
                sd2 += sd(lenLigne,i)

    for x in range(1,9):
        lenLigne = 9 - x
        y=0
        nodeValue = game.getNode(x,y).value
        if nodeValue != 0:
            if nodeValue == value:
                sd1 += sd(lenLigne,x)
            else:
                sd2 += sd(lenLigne,x)
        while x!=8:
            x+=1
            y+=1
            nodeValue = game.getNode(x,y).value
            if nodeValue != 0:
                if nodeValue == value:
                    sd1 += sd(lenLigne,x)
                else:
                    sd2 += sd(lenLigne,x)

    return sd1,sd2

def evalVar(game,value):
    """
    Fonction d'évaluation qui prend en compte les variables du joueur.
    game :game
    value : int
    """
    if game.isFinished():
        return 1000000

    var = game.vars[value]

    p1Score = 0                                     #var1          
    p2Score = 0                                     #var2                                
    difscore = 0                                    #var3

    if value == 0:
        p1Score = game.players[0].score - 20             
        p2Score = 140 - game.players[1].score       
        difscore = p1Score - p2Score
    elif value == 1:
        p1Score = game.players[0].score - 20             
        p2Score = 140 - game.players[1].score                
        difscore = p2Score - p1Score
    

    sd1,sd2 = sdMiddle(game,value)                  #var4 var5
    sd1,sd2 = sd1/100,sd2/100
    return sum([p1Score*var[0],p2Score*var[1],difscore*var[2],sd1*var[3],sd2*var[4]])

def tournament(players):
    """
    Play a tournament between all the players and return the winner
    players : list of players
    """
    #random beetwen 0 and 1
    while len(players) > 1:
        p1 = players.pop(0)
        p2 = players.pop(0)

        g = game.Game(-1,-1,p1,p2)
        while not g.isFinished():
            g.players[(g.turn-1)%2].agentPlay(g)

        if g.winner == 0:
            players.append(p1)
        else:
            players.append(p2)

    return players[0]

def validation(player):
    """
    Joue 10 parties contre un agent Greedy et retourne True si le joueur a gagné plus de 5 parties
    """
    w=0
    for _ in range(10):
        g = game.Game(2,-1,var2=player)
        while not g.isFinished():
            g.players[(g.turn-1)%2].agentPlay(g)
        if g.winner == 1:
            w+=1

    if w >=5:
        return True,w
    return False,w


def randomVar():
    return [round(uniform(-1,1),3) for _ in range(5)]

def genetic(nbPlayers,player=None):
    """
    Play a genetic algorithm with nbPlayers players
    nbPlayers : number of players
    player : if you want to start with a specific player
    """
    delta = 0.2
    lastValid = None
    nbW = 0

    if player == None:
        player = randomVar()
    else:
        lastValid = player
    players = []
    
    while True:    

        for _ in range((nbPlayers//10) *9):
            var = []
            for i in range(len(player)):
                var.append(player[i]+round(uniform(-delta,delta),3))
            players.append(var)
        
        for _ in range(nbPlayers//10):
            var = randomVar()
            players.append(var)

        player = tournament(players)

        for i in range(len(player)):
            player[i] = round(player[i],3)

        valid,w = validation(player)

        if valid and w > nbW:
            print("Ce joueur a battut le greedy!",player)
            lastValid = player
            nbW = w
            delta = delta*0.9
        else:
            print("Ce joueur est nul!", player)
            if lastValid != None:
                player = lastValid
            else:
                player = randomVar()



if __name__ == "__main__":
    """
    C'est ici qu'on lance l'algo génétique
    L'algo ne va jamais s'arreter, il faut donc l'arreter manuellement
    """
    #genetic(nbPlayers=10,player=[1,-1,5,-10,-10])

    #interface textuelle
    print(f"Bienvenue dans le laboratoire génétique !\n")
    print(f"Vous allez pouvoir tester votre agent génétique contre l'agent agent 002: Greedy\n")
    print(f"Vous pouvez arreter le programme à tout moment en appuyant sur Ctrl+C\n")

    print(f"Combien de joueurs voulez-vous tester ?")
    nbPlayers = int(input())
    print(f"Voulez-vous commencer avec un joueur spécifique ? (y/n)")
    try:
        if input() == "y":
            print(f"Entrez les valeurs de votre joueur (séparées par des espaces)")
            print(f"Par exemple : 1 -1 5 -10 -10")
            player = [float(i) for i in input().split()]
            genetic(nbPlayers=nbPlayers,player=player)
        else:
            genetic(nbPlayers) #random
    except KeyboardInterrupt:
        print(f"Vous avez arrêté le programme")
        exit(0)
