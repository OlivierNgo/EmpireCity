import pygame
import os, inspect
from pygame.transform import scale

#recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"data")


# Setup
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

police = pygame.font.SysFont("arial", 15)
 
 
print(scriptDIR)
 
 
# Set the width and height of the screen [width,height]
screeenWidth = 400
screenHeight = 300
screen = pygame.display.set_mode((screeenWidth,screenHeight))
 
pygame.display.set_caption("Empire City")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(True) 
 
# Image de fond
fond = pygame.image.load(os.path.join(assets, "map.png"))

# Image du viseur
viseur = pygame.image.load(os.path.join(assets, "viseur.png"))
 
 
# Définition des coordonnées du point S dans le repère du décor
point_S_x = 353  # Coordonnée x initiale du point S
point_S_y = 175  # Coordonnée y initiale du point S 

# Définition des valeurs initiales pour que le jeu commence sur le devant de l’église
point_S_x_initiale = 150  # Coordonnée x du devant de l'église
point_S_y_initiale = 380  # Coordonnée y du devant de l'église 

# Initialisation des coordonnées du point S pour commencer sur le devant de l’église
point_S_x = point_S_x_initiale
point_S_y = point_S_y_initiale


# Creation des variables pour stocker les coordonnées du point V
point_V_x = 0  # Coordonnée x initiale du point V
point_V_y = 0  # Coordonnée y initiale du point V

# Initialisation de V pour que le viseur se situe au milieu de la fenêtre de jeu
# Les coordonnées du point V seront au centre de l'écran moins la moitié de la taille du viseur
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
 
 
# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
   
   # récupère la liste des touches claviers appuyeées sous la forme liste bool
   pygame.event.pump()
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
      elif event.type == pygame.KEYDOWN:
           # Gestion des touches du clavier pour déplacer le viseur
           if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if point_V_y - viseur_speed < dead_zone_top:
                        point_S_y -= viseur_speed
                    else:
                        point_V_y -= viseur_speed
                elif event.key == pygame.K_DOWN:
                    if point_V_y + viseur_speed > dead_zone_bottom:
                        point_S_y += viseur_speed
                    else:
                        point_V_y += viseur_speed
                elif event.key == pygame.K_LEFT:
                    if point_V_x - viseur_speed < dead_zone_left:
                        point_S_x -= viseur_speed
                    else:
                        point_V_x -= viseur_speed
                elif event.key == pygame.K_RIGHT:
                    if point_V_x + viseur_speed > dead_zone_right:
                        point_S_x += viseur_speed
                    else:
                        point_V_x += viseur_speed
   
   

    # LOGIQUE
 
 

 
    # DESSIN
    
    
   # affiche la zone de rendu au dessus de fenetre de jeu
   zonejaune = pygame.Rect( point_S_x, point_S_y, screeenWidth, screenHeight )
   screen.blit(fond,(0,0),area = zonejaune)
   
   # Dessiner le viseur à l'écran
   screen.blit(viseur, (point_V_x, point_V_y))
   
  
    # Go ahead and update the screen with what we've drawn.
   pygame.display.flip()
 
    # Limit frames per second
   clock.tick(30)
 
# Close the window and quit.
pygame.quit()