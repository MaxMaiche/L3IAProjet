from copy import deepcopy
import itertools
import random
import agent
import sys
import cProfile	
import learningEval

sys.setrecursionlimit(100000)

class Node:
    """
    Classe qui représente une case du jeu
    game: le jeu
    x: la position x de la case
    y: la position y de la case
    value: la valeur de la case (0: vide, 1: joueur 1, 2: joueur 2)
    score: le score de la case
    voisins: les voisins de la case
    coupsValide: les coups valides pour la case
    """
    def __init__(self, game, x:int, y:int):
        self.game = game
        self.x = x
        self.y = y
        self.value = 0
        self.score = 0
        self.voisins = []
        self.coupsValide = set()
        
    def setVoisins(self)->None:
        """
        fonction qui initialise les voisins de la case
        """
        x=self.x
        y=self.y
        voisins = []
        if x > 0:
            voisins.append(self.game.getNode(x-1, y))
        else:
            voisins.append(None)
        if y > 0:
            voisins.append(self.game.getNode(x, y-1))
        else:
            voisins.append(None)
        if x < 8:
            voisins.append(self.game.getNode(x+1, y))
        else:
            voisins.append(None)
        if y < 8:
            voisins.append(self.game.getNode(x, y+1))
        else:
            voisins.append(None)
        if x > 0 and y > 0:
            voisins.append(self.game.getNode(x-1, y-1))
        else:
            voisins.append(None)
        if x < 8 and y < 8:
            voisins.append(self.game.getNode(x+1, y+1))
        else:
            voisins.append(None)
        
        self.voisins = voisins
        
    
    def getVoisin(self,i):
        """
        fonction qui retourne le voisin i de la case
        """
        return self.voisins[i]

    def getCoupsValide(self)->set:
        """
        fonction qui retourne les coups valides pour la case
        """
        coups = {self}
        nodes = [self]
        nodesSaut = []
        node = nodes.pop()
        for i in range(6):
            voisin = node.getVoisin(i)
            if voisin == None:
                continue
            if voisin.value == 0:
                coups.add(voisin)
            else:
                if voisin.getVoisin(i) != None and voisin.getVoisin(i).value == 0:
                    nodesSaut.append(voisin.getVoisin(i))
                    coups.add(voisin.getVoisin(i))
    
        coups = self.getCoupsSaut(coups,nodesSaut)
        coups.remove(self)
        self.coupsValide = coups
        return coups
    

    def getCoupsSaut(self, coups, nodes:list)->set:
        """
        fonction qui retourne les coups valides pour la case en sautant
        """
        
        while len(nodes) > 0:
            node = nodes.pop()
            for i in range(6):
                voisin = node.getVoisin(i)
                if voisin == None:
                    continue
                if voisin.value != 0:
                    if voisin.getVoisin(i) != None and voisin.getVoisin(i).value == 0 and voisin.getVoisin(i) not in coups:
                        nodes.append(voisin.getVoisin(i))
                        coups.add(voisin.getVoisin(i))
        return coups
    

    def __lt__ (self, other: 'Node'):
        """
        fonction qui compare deux cases
        """
        return self.score < other.score

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

class player:
    """
    Classe qui représente un joueur
    type: le type du joueur (0: joueur, 1: agentRandom, 2: agentGreedy, etc)
    score: le score du joueur
    pions: les pions du joueur
    coups: les coups valides du joueur
    """
    def __init__(self, value:int, type):
        self.type = type 
        self.value = value
        if value == 1:
            self.score = 20 # score de base du joueur
        else:
            self.score = 140 # score de base du joueur
        self.pions = set()
        self.coups = dict()

    def getCoups(self)->dict:
        """
        fonction qui retourne les coups valides du joueur
        """
        self.coups.clear()
        for pion in self.pions:
            self.coups[pion] = pion.getCoupsValide()
        return self.coups
    
    def getCoupsList(self)->list:
        """
        fonction qui retourne les coups valides du joueur sous forme de liste
        """
        coups = self.getCoups()
        
        list = []
        for key in coups:
            for v in coups[key]:
                list.append((key,v))
        return list
    

    def getCoupsListAndScore(self):
        """
        fonction qui retourne les coups valides du joueur sous forme de liste avec le score de chaque coup
        """
        coups = self.getCoupsList()
        coupsAndScore = []

        if self.value == 2:
            for coup in coups:
                score = coup[0].score - coup[1].score
                coupsAndScore.append((coup,score))
        else:
            for coup in coups:
                score = coup[1].score - coup[0].score
                coupsAndScore.append((coup,score))
                
                                     
        coupsAndScore = sorted(coupsAndScore, key=lambda x: x[1], reverse=True)
        return coupsAndScore
                

    def play(self, node:Node, node2:Node,game)->bool:
        """
        fonction qui joue un coup
        node: la case de départ
        node2: la case d'arrivée
        """
        node.value = 0
        node2.value = self.value

        score = node.score - node2.score
        self.score -= score

        self.pions.remove(node)
        self.pions.add(node2)

        if game.isFinished():
            return True
        game.turn += 1
        return False

    def undo(self, node:Node, node2:Node,game)->None:
        """
        fonction qui annule un coup
        node: la case de départ
        node2: la case d'arrivée
        """
        node2.value = 0
        node.value = self.value

        score = node.score - node2.score
        self.score += score

        self.pions.remove(node2)
        self.pions.add(node)

        game.turn -= 1
        game.end = False

    def isHuman(self)->bool:
        """
        fonction qui retourne si le joueur est humain
        """
        return self.type == 0

    def agentPlay(self, game)->None:
        """
        fonction qui fait jouer l'agent
        """
        if self.type == -1:
            learningEval.greedyAgentVar(game,self.value)
        if self.type == -2:
            learningEval.alpha_Beta_Agent_Var(game,self.value,2)
        if self.type == 1:
            game.end = agent.randomAgent(game, self.value)
        elif self.type == 2:
            game.end = agent.greedyAgent(game,self.value)
        elif self.type == 3:
            game.end = agent.minimaxAgent(game,self.value, 3)
        elif self.type >= 4:
            profondeur = self.type - 3
            game.end = agent.alpha_Beta_Agent(game,self.value,profondeur)
        


class Game:
    """
    Classe qui représente une partie
    end: si la partie est terminée
    draw: si la partie est nulle
    board: le plateau de jeu
    turn: le tour actuel
    winner: le gagnant
    memo: le dictionnaire qui contient les états déjà visités
    players: les joueurs
    """
    def __init__(self, type1, type2, var1=None, var2=None):
        if type1 == -100 and type2 == -100:
            return
        self.end = False
        self.draw = False
        self.board = []
        self.turn = 1
        self.winner = None
        self.memo = dict()

        self.vars = [var1,var2]
        self.players = []
        self.players.append(player(1, type1))
        self.players.append(player(2, type2))

        for x,y in itertools.product(range(9), range(9)):
            self.board.append(Node(self,x,y))
        
        for i in range(81):
            self.board[i].setVoisins()
        
        for y in range(4):
            for x in range(5+y, 9):
                node = self.getNode(x,y)
                node.value = 1
                self.players[0].pions.add(node)
 
        for x in range(4):
            for y in range(5+x, 9):
                node = self.getNode(x,y)
                node.value = 2
                self.players[1].pions.add(node)

        
        for y in range(8,0,-1):
            score = 8+y
            x=0
            self.getNode(x,y).score = score
            while y!=8:
                x+=1
                y+=1
                self.getNode(x,y).score = score
        
        for i in range(0,9):
            self.getNode(i,i).score = 8
        
        for x in range(1,9):
            score = 8-x
            y=0
            self.getNode(x,y).score = score
            while x!=8:
                x+=1
                y+=1
                self.getNode(x,y).score = score
            
    def __deepcopy__(self, memo):
        """
        override de la fonction deepcopy pour avoir la main sur la copie et son contenu
        car deepcopy est très couteux en temps
        """
        game = Game(-100,-100)
        game.end = self.end
        game.draw = self.draw
        game.board = deepcopy(self.board, memo)
        game.turn = self.turn
        game.winner = self.winner
        game.memo = None
        game.players = deepcopy(self.players, memo)
        game.vars = self.vars
        return game

    def getBoard(self)->list:
        """
        fonction qui retourne le plateau de jeu
        """
        return self.board

    def getNode(self, x, y) -> Node:
        """
        fonction qui retourne le noeud aux coordonnées x,y
        """
        if x<0 or x>8 or y<0 or y>8:
            return None
        return self.board[x*9+y]
    
   
 
    def print(self):
        """
        fonction qui affiche le plateau de jeu en console
        """
        for y in range(8,0,-1):
            
            chaine = "  " * y
            x=0
            chaine += str(self.getNode(x,y).value)
            while y!=8:
                x+=1
                y+=1
                chaine+= "  " + str(self.getNode(x,y).value)
            print(chaine)
        
        print("".join([str(self.getNode(i,i).value)+"  " for i in range(0,9) ]))
        
        for x in range(1,9):
            
            chaine = "  " * x
            y=0
            chaine += str(self.getNode(x,y).value)
            while x!=8:
                x+=1
                y+=1
                chaine+= "  " + str(self.getNode(x,y).value)
            print(chaine)
            
    def isFinished(self)->bool:
        """
        fonction qui retourne si la partie est terminée
        """
        if self.turn == 350:
            self.end = True
            p1Score = self.players[0].score
            p2Score = 140 - self.players[1].score
            
            if p1Score > p2Score:
                self.winner = 0
            elif p2Score > p1Score:
                self.winner = 1
            else:
                self.draw = True
        
        if self.players[0].score == 140:
            self.end = True
            self.winner = 0
        
        if self.players[1].score == 20:
            self.end = True
            self.winner = 1

        return self.end
    
    def eval(self, value):
        """
        fonction qui retourne la valeur de l'état actuel
        """
        score = 0
        p1Score = self.players[0].score
        p2Score = 140 - self.players[1].score

        
        if value == 0:
            score = p1Score - p2Score
        elif value == 1:
            score = p2Score - p1Score
        return score

    def split(self)->bool:
        """
        fonction qui retourne si l'état actuel est un split
        un split est un état ou l'action d'un joueur n'a pas d'impact sur les coups possibles de l'autre joueur
        """

        minP1 = 1000
        minP2 = 1000
        maxP1 = -1000
        maxP2 = -1000

        for pion in self.players[0].pions:
            if pion.score < minP1:
                minP1 = pion.score
            #if pion.score > maxP1:
            #    maxP1 = pion.score
        
        for pion in self.players[1].pions:
            #if pion.score < minP2:
            #    minP2 = pion.score
            if pion.score > maxP2:
                maxP2 = pion.score
        
        #if maxP1+2 < minP2:
        #    return True
        if maxP2+2 < minP1:
            return True
        else:
            return False

    def hash(self)->int:
        """
        fonction qui retourne le hash de l'état actuel
        """
        h = 0
        for node in self.board:
            h = h*3 + node.value
        
        if self.turn%2 == 0:
            h=-h

        return h 

def sanityCheck(game:Game):
    """
    fonction qui vérifie si les coups possibles sont bien les bons
    """
    for _ in range(10):
        test= []
        for i in range(10):
            test.append(1)
        for i in range(10):
            test.append(2)
        for i in range(61):
            test.append(0)
        random.shuffle(test)

        for i in range(81):
            game.board[i].value = test[i]

        node = 0
        for i in range(81):
            if game.board[i].value == 1:
                node = game.board[i]
                break
        
        coups = node.getCoupsValide()
        for coup in coups:
            game.getNode(coup.x,coup.y).value = "X"
        
        node.value = "#"
        game.print()
        
def sanityCheck2(game:Game):
    """
    fonction qui vérifie le nombre de collision de hash
    """
    memoBoard = set()
    memoHash = set()
    nbCollision = 0
    for _ in range(100000):
        test= []
        for i in range(10):
            test.append(1)
        for i in range(10):
            test.append(2)
        for i in range(61):
            test.append(0)
        random.shuffle(test)

        if tuple(test) in memoBoard:
            continue
        else:
            memoBoard.add(tuple(test))

        for i in range(81):
            game.board[i].value = test[i]
        
        h = game.hash()
        if h in memoHash:
            nbCollision += 1
        else:
            memoHash.add(h)

    print("nbCollision : " + str(nbCollision))

def winrateCheck(agent1, agent2, nbGame:int):
    """
    fonction qui vérifie le winrate de l'agent1 contre l'agent2
    """
    winrate = 0
    drawcount = 0
    sumTurn = 0
    for i in range(nbGame):
        g = Game(agent1, agent2)
        while not g.isFinished():
            g.players[(g.turn-1)%2].agentPlay(g)
        
        sumTurn += g.turn
        if g.draw:
            drawcount += 1
            print("game " + str(i) + " finished Draw")
            continue
        if g.players[0].score == 140 :
            winrate += 1
            print("game " + str(i) + " finished Win")
        else:
            print("game " + str(i) + " finished Lose")
    print("winrate : " + str(winrate/nbGame * 100) + "%")
    print("draw : " + str(drawcount/nbGame * 100) + "%")
    #print("avg turn : " + str(sumTurn/nbGame))


def main(type1, type2, nbGame:int):
    """
    fonction qui lance le programme
    """
    winrateCheck(type1, type2, nbGame) 


if __name__ == "__main__":
    """
    C'est ici que l'on lance le programme en console
    """
    #interface textuelle
    print(f"Bienvenue dans le jeu de dames chinoises !\n")
    #liste des types de joueurs
    print(f"Liste des types de joueurs :")

    print(f"1 : Random")
    print(f"2 : Greedy")
    print(f"3 : Minimax")
    print(f"4+n : Alphabeta + profondeur n (4=1, 5=2, 6=3 etc)")
    print(f"Choisissez le type de joueur 1 :")
    type1 = int(input())

    print(f"Choisissez le type de joueur 2 :")
    type2 = int(input())
    print(f"Choisissez le nombre de parties :")

    nbGame = int(input())

    main(type1=type1, type2=type2, nbGame=nbGame) 
    # 1 = random, 2 = greedy,3 = minimax , 4+n = alphabeta + profondeur (4=1, 5=2, 6=3 etc)


    # g = Game(0,1)
    # g.print()
    # sanityCheck(g) 
    # sanityCheck2(g)

    #cProfile.run('main()')

    