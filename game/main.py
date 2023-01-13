import itertools


class Node:
    def __init__(self, game, x:int, y:int):
        self.game = game
        self.x = x
        self.y = y
        self.value = 0
        self.voisins = []
        
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

    def coupsValide(self)->set:
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
    
        coups = coups.union(self.getCoupsSaut(nodesSaut))
        return coups
    
    def getCoupsSaut(self,nodes:list)->set:
        coups=set()

        while len(nodes) > 0:
            node = nodes.pop()
            for i in range(6):
                voisin = node.getVoisin(i)
                if voisin == None:
                    continue
                if voisin.value != 0:
                    if voisin.getVoisin(i) != None and voisin.getVoisin(i).value == 0:
                        nodes.append(voisin)
                        coups.add(voisin)
        return coups
    
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
        
class Game:
    def __init__(self):
        self.end = False
        self.board = []
        for x,y in itertools.product(range(9), range(9)):
            self.board.append(Node(self,x,y))
        
        for i in range(81):
            self.board[i].setVoisins()
        
        for y in range(4):
            for x in range(5+y, 9):
                node = self.getNode(x,y)
                node.value = 1
                
        for x in range(4):
            for y in range(5+x, 9):
                node = self.getNode(x,y)
                node.value = 2
        
    
    def getNode(self, x, y) -> Node:
        if x<0 or x>8 or y<0 or y>8:
            return None
        return self.board[x*9+y]
    
    
    def printBoard(self) -> None:
        for y in range(9):
            for x in range(9):
                node = self.getNode(x,y)
                if node.value == 0:
                    print("#", end="  ")
                elif node.value == 1:
                    print("X", end="  ")
                elif node.value == 2:
                    print("O", end="  ")
            print()
            
            
 
    def printPyramides(self):
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
            

g = Game()

coups = g.getNode(6,1).coupsValide()
for c in coups:
    c.value="X"

g.printPyramides()      
