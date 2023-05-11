import sys
import pygame
import game
from screeninfo import get_monitors

sys.setrecursionlimit(100000)

pygame.init()

#Pour scale la fenetre en fonction de la taille de l'ecran
HEIGHT= get_monitors()[0].height - 100
if HEIGHT > 1000:
    HEIGHT = 1000
WIDTH = int(HEIGHT*0.7)-50
#WIDTH, HEIGHT = 700, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dames Chinoises")

FPS = 144

def draw_line(game, list:list, ligne:int, circles:list):
    """
    fonction qui dessine une ligne du plateau de jeu
    """
    circle_size = 40
    total_width = (len(list) * circle_size) + ((len(list) - 1) * 20)
    x = (WIDTH - total_width) / 2


    for element in list:
        val = game.getNode(element[0],element[1]).value
        if val == 1:
            color = (255,0,0)
            
        elif val == 2:
            color = (0,0,0)
        else:
            color = (255,255,255)

        circles.append((x, ligne, val, element[0], element[1]))
        pygame.draw.circle(WIN, color, (x, ligne), 25)
        
        x += circle_size + 20

def draw_board(game, circles:list):
    """
    fonction qui dessine le plateau de jeu
    """
    line = 70
    for y in range(8,0,-1):
        x=0
        list = [(x,y)]
        while y!=8:
            x+=1
            y+=1
            list.append((x,y))

        draw_line(game,list, line, circles)
        line += 50
            
            
    list = [(x,x) for x in range(9)]
    draw_line(game,list, line, circles)
    line += 50
    
      
    for x in range(1,9):
        y=0
        list = [(x,y)]
        while x!=8:
            x+=1
            y+=1
            list.append((x,y))
        draw_line(game, list, line, circles)
        line += 50

def draw_coupsValide(coups:set, circles:list):
    """
    fonction qui dessine les coups valides
    """
    for node in coups:
        x = node.x
        y = node.y
        for _, (x2, y2, _, node_x, node_y) in enumerate(circles):
            if x == node_x and y == node_y:
                pygame.draw.circle(WIN, (100,100,100), (x2, y2), 25)
                break


def draw_window(game,circles:list, coups:set):
    """
    fonction principale qui dessine la fenetre
    """
    WIN.fill((15,85,200))
    circles.clear()

    draw_board(game, circles)
    draw_coupsValide(coups, circles)

    if game.end:
        font = pygame.font.SysFont('comicsans', 75)
        text = font.render('Fin de la partie', 1, (255,0,255))
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))

    pygame.display.update()

def wait(time):
    """
    fonction qui attend un certain temps
    """
    pygame.time.wait(int(time*1000))

def main(game):
    """
    fonction qui lance l'interface graphique
    """
    clock = pygame.time.Clock()
    run = True
    circles = []
    node_depart = None
    coups=set()
    sec = 0.01
    
   
    while run:
        clock.tick(FPS)

        #parcours des event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and game.players[1-game.turn%2].isHuman() and (not game.end):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, (x, y, val, node_x, node_y) in enumerate(circles):
                    if (x - mouse_x) ** 2 + (y - mouse_y) ** 2 <= 25 ** 2:
                        if val >= 1 and val%2 == game.turn%2: #circle has the current player's color, display targets
                            node_depart = game.getNode(node_x, node_y)
                            coups = node_depart.getCoupsValide()
                        elif val == 0 and node_depart != None:
                            node_target = game.getNode(node_x, node_y)
                            if node_target not in coups:
                                break
                            game.players[1-game.turn%2].play(node_depart, node_target, game)
                            coups = set()
                            node_depart = None
        # agent play si besoin
        if run and (not game.players[1-game.turn%2].isHuman()) and (not game.end) : 
            game.players[1-game.turn%2].agentPlay(game)       
            wait(sec)
             

        draw_window(game, circles, coups)
    pygame.quit()


if __name__ == "__main__":
    """C'est ici pour lancer le jeu avec l'interface graphique"""

    #interface textuelle
    print(f"Bienvenue dans le jeu de dames chinoises !\n")
    #liste des types de joueurs
    print(f"Liste des types de joueurs :")
    print(f"0 : Humain")
    print(f"1 : Random (déconseillé)")
    print(f"2 : Greedy")
    print(f"3 : Minimax")
    print(f"4+n : Alphabeta + profondeur n (4=1, 5=2, 6=3 etc)")
    print(f"Choisissez le type de joueur 1 :")
    type1 = int(input())

    print(f"Choisissez le type de joueur 2 :")
    type2 = int(input())

    game = game.Game(type1=type1, type2=type2) #0 = joueur, 1 = random, 2 = greedy,3 = minimax , 4+n = alphabeta + profondeur (4=1, 5=2, 6=3 etc)
    main(game)
