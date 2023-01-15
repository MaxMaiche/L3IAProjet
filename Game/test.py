import pygame

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH = 800
HEIGHT = 600
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialisation de la matrice de jeu et des variables de jeu
matrix = [[None for _ in range(8)] for _ in range(8)]
selected_circle = None
valid_moves = []

# Liste des cercles à dessiner
circles = []
for i in range(5):
    x = 50 + i * 100
    y = 50
    r = 25
    circles.append((x, y, r))

# Boucle principale
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifie si l'utilisateur clique sur un cercle
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, (x, y, r) in enumerate(circles):
                if (x - mouse_x) ** 2 + (y - mouse_y) ** 2 <= r ** 2:
                    if selected_circle is None:
                        # Sélectionner le cercle si aucun n'est sélectionné
                        selected_circle = i
                        # Calculer les coups valides pour le cercle sélectionné
                        valid_moves = get_valid_moves(matrix, i)
                    elif i in valid_moves:
                        # Déplacer le cercle sélectionné à l'emplacement cliqué
                        matrix[i] = matrix[selected_circle]
                        matrix[selected_circle] = None
                        circles[i] = circles[selected_circle]
                        # Reset des variables de jeu
                        selected_circle = None
                        valid_moves = []

    # Dessiner les cercles
    fenetre.fill((255, 255, 255))  # remplir la fenêtre en blanc
    for i, (x, y, r) in enumerate(circles):
        if i == selected_circle:
            color = (255, 0, 0)  # rouge pour le cercle sélectionné
        elif i in valid_moves:
            color = (0, 255, 0)  # vert pour les emplacements valides
        else:
            color = (0, 0, 0)  # noir pour les autres cercles
        pygame.draw.circle(fenetre, color, (x, y), r)

    pygame.display.flip()

# Quitter pygame
pygame.quit()
