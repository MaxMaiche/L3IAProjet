import pygame
import game
import agent
from screeninfo import get_monitors
pygame.init()

HEIGHT= get_monitors()[0].height - 100
WIDTH = int(HEIGHT*0.7)-50
#WIDTH, HEIGHT = 700, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dames Chinoises")

FPS = 60

def draw_line(game, list:list, ligne:int, circles:list):
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
    for node in coups:
        x = node.x
        y = node.y
        for _, (x2, y2, _, node_x, node_y) in enumerate(circles):
            if x == node_x and y == node_y:
                pygame.draw.circle(WIN, (100,100,100), (x2, y2), 25)
                break


def draw_window(game,circles:list, coups:set):
    WIN.fill((15,85,200))
    circles.clear()

    draw_board(game, circles)
    draw_coupsValide(coups, circles)

    if game.end:
        font = pygame.font.SysFont('comicsans', 100)
        text = font.render('Fin de la partie', 1, (255,0,255))
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))

    pygame.display.update()

def wait(time):
    pygame.time.wait(int(time*1000))

def main(game):
    clock = pygame.time.Clock()
    run = True
    circles = []
    node_actuel = None
    coups=set()
    while run:

        clock.tick(FPS)

        if game.end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            draw_window(game, circles, coups)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and game.turn%2 == 1 and game.joueur1.type == 0:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                trouve = False
                for i, (x, y, val, node_x, node_y) in enumerate(circles):
                    if (x - mouse_x) ** 2 + (y - mouse_y) ** 2 <= 25 ** 2:
                        if val == 1:
                            node_actuel = game.getNode(node_x, node_y)
                            coups = node_actuel.getCoupsValide()
                            trouve = True
                            break
                        elif val == 0 and node_actuel != None:
                            node = game.getNode(node_x, node_y)
                            if node in coups:
                                game.end = game.joueur1.play(node_actuel, node, game)
                                    
                                node_actuel = None
                                coups = set()
                                trouve = True
                                break
                        
                if not trouve:
                    coups = set()

        sec = 0.1
        if game.turn%2 == 1:
            if game.joueur1.type == 1:
                game.end = agent.randomAgent(game,1)
                wait(sec)
            if game.joueur1.type == 2:
                game.end = agent.greedyAgent(game,1)
                wait(sec)

        if game.turn%2 == 0:
            if game.joueur2.type == 1:
                game.end = agent.randomAgent(game,2)
                wait(sec)
            if game.joueur2.type == 2:
                game.end = agent.greedyAgent(game,2)
                wait(sec)

        draw_window(game, circles, coups)

    pygame.quit()

if __name__ == "__main__":
    game = game.Game(2,2) #0 = joueur, 1 = random, 2 = greedy
    main(game)