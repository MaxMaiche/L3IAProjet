import itertools
import random


class Node:
    def __init__(self, game, x:int, y:int):
        self.game = game
        self.x = x
        self.y = y
        self.value = 0
        self.score = 0
        self.voisins = []
        self.coupsValide = set()
        
    def setVoisins(self)->None:
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
        return self.voisins[i]

    def getCoupsValide(self)->set:
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
    
    def getCoupsSaut(self,coups,nodes:list)->set:
        
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

    def __lt__ (self, other):
        return self.score < other.score

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

class player:
    def __init__(self, value:int, type):
        self.type = type # 0 = joueur, 1 = agentRandom , 2 = agentGreedy
        self.value = value
        if value == 1:
            self.score = 20 # score de base du joueur
        else:
            self.score = 140 # score de base du joueur
        self.pions = set()
        self.coups = dict()

    def getCoups(self)->dict:
        self.coups.clear()
        for pion in self.pions:
            self.coups[pion] = pion.getCoupsValide()
        return self.coups
    
    def getCoupsScore(self)->dict:
        self.coups.clear()
        for pion in self.pions:
            self.coups[pion] = pion.getCoupsScore()
        return self.coups

    
    def play(self, node:Node, node2:Node,game)->bool:
        node.value = 0
        node2.value = self.value

        score = node.score - node2.score
        self.score -= score

        self.pions.remove(node)
        self.pions.add(node2)
        self.getCoups()
        if game.isFinished():
            return True
        game.turn += 1
        return False


class Game:
    def __init__(self, type1, type2):
        self.end = False
        self.board = []
        self.turn = 1
        self.joueurs = []
        self.joueurs.append(player(1, type1))
        self.joueurs.append(player(2, type2))

        for x,y in itertools.product(range(9), range(9)):
            self.board.append(Node(self,x,y))
        
        for i in range(81):
            self.board[i].setVoisins()
        
        for y in range(4):
            for x in range(5+y, 9):
                node = self.getNode(x,y)
                node.value = 1
                self.joueurs[0].pions.add(node)
                
        for x in range(4):
            for y in range(5+x, 9):
                node = self.getNode(x,y)
                node.value = 2
                self.joueurs[1].pions.add(node)

        
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
            
                
    def getBoard(self)->list:
        return self.board

    def getNode(self, x, y) -> Node:
        if x<0 or x>8 or y<0 or y>8:
            return None
        return self.board[x*9+y]
    
   
 
    def print(self):
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
        if self.joueurs[0].score == 140:
            self.end == True
            return True
        
        if self.joueurs[1].score == 20:
            self.end = True
            return True

        return self.end

def sanityCheck(game:Game):

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
        

if __name__ == "__main__":
    g = Game(0,0)
    g.print()
    sanityCheck(g) 