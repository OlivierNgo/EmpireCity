import pygame
import os, inspect
import random

# Recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data")

# Setup
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

police = pygame.font.SysFont("arial", 15)

print(scriptDIR)

# Taille de la fenetre
screeenWidth = 600
screenHeight = 400
screen = pygame.display.set_mode((screeenWidth, screenHeight))

pygame.display.set_caption("Empire City")

# Vairables de direction
move_up = False
move_down = False
move_left = False
move_right = False

done = False

clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(True)

# Image de fond
fond = pygame.image.load(os.path.join(assets, "map.png"))
map_width = fond.get_width()  # Obtaining the map width
map_height = fond.get_height()  # Obtaining the map height

# Image du bandit
bandit = pygame.image.load(os.path.join(assets, "bandit_rue.png"))

# Image du viseur
viseur = pygame.image.load(os.path.join(assets, "viseur.png"))

bang = pygame.image.load(os.path.join(assets, "bang.png"))

# Définition des coordonnées du point S dans le repère du décor
point_S_x = 150  # Coordonnée x initiale du point S (devant de l’église)
point_S_y = 285  # Coordonnée y initiale du point S (devant de l’église)

# Initialisation de V pour que le viseur se situe au milieu de la fenêtre de jeu
point_V_x = (screeenWidth // 2) - (viseur.get_width() // 2)
point_V_y = (screenHeight // 2) - (viseur.get_height() // 2)

viseur_speed = 5

# Définir la taille de la zone morte (zone orange)
dead_zone_width = screeenWidth // 3
dead_zone_height = screenHeight // 3

# Définir les limites de la zone morte
dead_zone_left = (screeenWidth - dead_zone_width) // 2.4
dead_zone_right = dead_zone_left + dead_zone_width
dead_zone_top = (screenHeight - dead_zone_height) // 2.6
dead_zone_bottom = dead_zone_top + dead_zone_height

# Sauvegarde de la valeur de l'horloge au démarrage et pour le respawn du bandit
T0 = pygame.time.get_ticks()
bandit_timer = None

# Initialisation de la position du bandit
bandit_x = None
bandit_y = None
bandit_visible = False

# -------- Main Program Loop -----------
while not done:
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
            elif event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_SPACE:  # Ajout pour la touche ESPACE
                # Vérifier la collision avec le bandit
                if bandit_visible:
                    bandit_rect = pygame.Rect(bandit_x - point_S_x, bandit_y - point_S_y, bandit.get_width(), bandit.get_height())
                    viseur_rect = pygame.Rect(point_V_x, point_V_y, viseur.get_width(), viseur.get_height())
                    if bandit_rect.colliderect(viseur_rect):
                        # Le viseur a touché le bandit, le bandit disparaît
                        bandit_visible = False
                        # Réinitialiser le timer pour faire apparaître un nouveau bandit
                        bandit_timer = pygame.time.get_ticks()
                # Afficher l'image "bang.png" à la position du viseur
                screen.blit(bang, (point_V_x, point_V_y))
                # Déplacer le viseur vers le haut
                point_V_y -= 20  # Ajustez la valeur selon votre préférence
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
            elif event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    # Deplacement dans la boucle principale
    if move_up:
        if point_V_y - viseur_speed < dead_zone_top:
            new_y = point_S_y - viseur_speed
            if new_y >= 0:
                point_S_y = new_y
        else:
            point_V_y -= viseur_speed
    if move_down:
        if point_V_y + viseur_speed > dead_zone_bottom:
            new_y = point_S_y + viseur_speed
            if new_y <= map_height - screenHeight:
                point_S_y = new_y
        else:
            point_V_y += viseur_speed
    if move_left:
        if point_V_x - viseur_speed < dead_zone_left:
            new_x = point_S_x - viseur_speed
            if new_x >= 0:
                point_S_x = new_x
        else:
            point_V_x -= viseur_speed
    if move_right:
        if point_V_x + viseur_speed > dead_zone_right:
            new_x = point_S_x + viseur_speed
            if new_x <= map_width - screeenWidth:
                point_S_x = new_x
        else:
            point_V_x += viseur_speed

    zonejaune = pygame.Rect(point_S_x, point_S_y, screeenWidth, screenHeight)
    screen.blit(fond, (0, 0), area=zonejaune)

    # Apparition du bandit après 3 secondes après le démarrage du jeu
    if pygame.time.get_ticks() - T0 >= 3000 and bandit_x is None and bandit_y is None:
        bandit_x = random.random() * (screeenWidth - bandit.get_width())
        bandit_y = 500 #Niveau du trottoir
        bandit_visible = True

    # Affichage du bandit lorsqu'il a été initialisé et est visible
    if bandit_visible:
        screen.blit(bandit, (bandit_x - point_S_x, bandit_y - point_S_y))

    screen.blit(viseur, (point_V_x, point_V_y))

    # Dessiner l'image "bang.png" si la touche ESPACE est pressée
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        screen.blit(bang, (point_V_x + 10, point_V_y + 10))

    # Actualiser l'écran
    pygame.display.flip()

    # Apparition du bandit après un certain délai après la mort du précédent
    if bandit_timer is not None and pygame.time.get_ticks() - bandit_timer >= 3000:
        bandit_x = random.random() * (screeenWidth - bandit.get_width())
        bandit_y = 500  # Niveau du trottoir
        bandit_visible = True
        bandit_timer = None  # Réinitialiser le timer


    

    # Update the screen
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()