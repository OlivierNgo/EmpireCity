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

# Set the width and height of the screen [width, height]
screeenWidth = 600
screenHeight = 400
screen = pygame.display.set_mode((screeenWidth, screenHeight))

pygame.display.set_caption("Empire City")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
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

# Sauvegarde de la valeur de l'horloge au démarrage
T0 = int(pygame.time.get_ticks()/1000)

# Initialisation de la position du bandit
bandit_x = None
bandit_y = None

# -------- Main Program Loop -----------
while not done:
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if point_V_y - viseur_speed < dead_zone_top:
                    new_y = point_S_y - viseur_speed
                    if new_y >= 0:  # Ensure the map doesn't move out of bounds
                        point_S_y = new_y
                else:
                    point_V_y -= viseur_speed
            elif event.key == pygame.K_DOWN:
                if point_V_y - viseur_speed > dead_zone_bottom:
                    new_y = point_S_y + viseur_speed
                    if new_y <= map_height - screenHeight:  # Ensure the map doesn't move out of bounds
                        point_S_y = new_y
                else:
                    point_V_y += viseur_speed
            elif event.key == pygame.K_LEFT:
                if point_V_x - viseur_speed < dead_zone_left:
                    new_x = point_S_x - viseur_speed
                    if new_x >= 0:  # Ensure the map doesn't move out of bounds
                        point_S_x = new_x
                else:
                    point_V_x -= viseur_speed
            elif event.key == pygame.K_RIGHT:
                if point_V_x - viseur_speed > dead_zone_right:
                    new_x = point_S_x + viseur_speed
                    if new_x <= map_width - screeenWidth:  # Ensure the map doesn't move out of bounds
                        point_S_x = new_x
                else:
                    point_V_x += viseur_speed

    # Draw the background and the cursor
    zonejaune = pygame.Rect(point_S_x, point_S_y, screeenWidth, screenHeight)
    screen.blit(fond, (0, 0), area=zonejaune)
    screen.blit(viseur, (point_V_x, point_V_y))

    # Apparition du bandit apres 3 secondes apres le demarrage du jeu
    current_time = int(pygame.time.get_ticks()/1000)
    if current_time - T0 >= 3 and bandit_x is None:
        bandit_x = random.random() * screeenWidth
        bandit_y = 200
        screen.blit(bandit, (bandit_x, bandit_y))

    # Affichage du bandit lorsqu'il a ete initialiser
    if bandit_x is not None and bandit_y is not None:
        screen.blit(bandit, (bandit_x, bandit_y))
    

    # Update the screen
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()