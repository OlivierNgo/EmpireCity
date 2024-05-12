import pygame
import os, inspect
import random

def Victoire(screen):
    win_text = pygame.font.SysFont("comicsansms", 48, bold=True).render("VICTOIRE !", True, WHITE)
    win_rect = win_text.get_rect(center=(screeenWidth // 2, screenHeight // 2))
    #Fond transparent
    overlay = pygame.Surface((screeenWidth, screenHeight), flags=pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    for alpha in range(0, 255, 15):
        win_text.set_alpha(alpha)
        screen.blit(win_text, win_rect)
        pygame.display.flip()
        pygame.time.wait(100)
    pygame.time.wait(5000)

def Fond(screen, text, font, color, x, y):
    shadow_color = (0, 0, 0)  # Noir pour l'ombre
    # Dessiner l'ombre légèrement décalée
    shadow_text = font.render(text, True, shadow_color)
    screen.blit(shadow_text, (x + 2, y + 2))
    # Dessiner le texte principal
    main_text = font.render(text, True, color)
    screen.blit(main_text, (x, y))

# Recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))
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
# Charger une police dynamique et colorée
score_font = pygame.font.SysFont("comicsansms", 28, bold=True)

print(scriptDIR)

# Taille de la fenetre
screeenWidth = 600
screenHeight = 400
screen = pygame.display.set_mode((screeenWidth, screenHeight))

pygame.display.set_caption("Empire City")

# Variables de direction
move_up = False
move_down = False
move_left = False
move_right = False

done = False

clock = pygame.time.Clock()

# Cacher la souris
pygame.mouse.set_visible(True)

# Image de fond
fond = pygame.image.load(os.path.join(assets, "map.png"))
map_width = fond.get_width()
map_height = fond.get_height()

# Images des bandits
bandit = pygame.image.load(os.path.join(assets, "bandit_rue.png"))
bandit_window = pygame.image.load(os.path.join(assets, "bandit_window4.png"))

# Image du viseur
viseur = pygame.image.load(os.path.join(assets, "viseur.png"))

# Animation du tir
bang = pygame.image.load(os.path.join(assets, "bang.png"))

# Image d'une balle
bullet = pygame.image.load(os.path.join(assets, "bullet.png"))
bullet_count = 6

# Coordonnées initiales
point_S_x = 150
point_S_y = 285
point_V_x = (screeenWidth // 2) - (viseur.get_width() // 2)
point_V_y = (screenHeight // 2) - (viseur.get_height() // 2)

# Vitesse du viseur
viseur_speed = 5

# Zone morte
dead_zone_width = screeenWidth // 3
dead_zone_height = screenHeight // 3
dead_zone_left = (screeenWidth - dead_zone_width) // 2.4
dead_zone_right = dead_zone_left + dead_zone_width
dead_zone_top = (screenHeight - dead_zone_height) // 2.6
dead_zone_bottom = dead_zone_top + dead_zone_height

T0 = pygame.time.get_ticks()
bandit_timer = None

# Bandit visible
bandit_x = None
bandit_y = None
bandit_visible = False

# Flèches
fleche_gauche = pygame.image.load(os.path.join(assets, "fleche_gauche.png"))
fleche_droite = pygame.image.load(os.path.join(assets, "fleche_droite.png"))
affichage_gauche = False
affichage_droite = False

# Coordonnées des fenêtres
window_positions = [
    (790, 285),  # Fenêtre 1
    (960, 285),  # Fenêtre 2
    (1200, 450), # Fenêtre 3
]

score = 0

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
            elif event.key == pygame.K_SPACE:
                if bullet_count > 0:
                    if bandit_visible:
                        bandit_rect = pygame.Rect(bandit_x - point_S_x, bandit_y - point_S_y, bandit.get_width(), bandit.get_height())
                        viseur_rect = pygame.Rect(point_V_x, point_V_y, viseur.get_width(), viseur.get_height())
                        if bandit_rect.colliderect(viseur_rect):
                            bandit_visible = False
                            bandit_timer = pygame.time.get_ticks()
                            score += 10
                    screen.blit(bang, (point_V_x, point_V_y))
                    point_V_y -= 20
                    bullet_count -= 1
            elif event.key == pygame.K_r:
                bullet_count = 6
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
            elif event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    # Déplacement du viseur
    if move_up:
        if point_V_y - viseur_speed < dead_zone_top:
            new_y = point_S_y - viseur_speed
            if new_y >= 0:
                point_S_y = new_y
        else:
            point_V_y -= viseur_speed
    if move_down:
        if point_V_y + viseur_speed > dead_zone_bottom and point_S_y < map_height - screenHeight:
            new_y = point_S_y + viseur_speed
            if new_y <= map_height - screenHeight:
                point_S_y = new_y
        else:
            point_V_y += viseur_speed
    if move_left:
        if point_V_x - viseur_speed < dead_zone_left and point_S_x > 0:
            new_x = point_S_x - viseur_speed
            if new_x >= 0:
                point_S_x = new_x
        else:
            point_V_x -= viseur_speed
    if move_right:
        if point_V_x + viseur_speed > dead_zone_right and point_S_x < map_width - screeenWidth:
            new_x = point_S_x + viseur_speed
            if new_x <= map_width - screeenWidth:
                point_S_x = new_x
        else:
            point_V_x += viseur_speed

    if point_V_x < 0:
        point_V_x = 0
    elif point_V_x > screeenWidth - viseur.get_width():
        point_V_x = screeenWidth - viseur.get_width()

    if point_V_y < 0:
        point_V_y = 0
    elif point_V_y > screenHeight - viseur.get_height():
        point_V_y = screenHeight - viseur.get_height()

    zonejaune = pygame.Rect(point_S_x, point_S_y, screeenWidth, screenHeight)
    screen.blit(fond, (0, 0), area=zonejaune)

    # Gestion de l'apparition du bandit
    if pygame.time.get_ticks() - T0 >= 3000 and bandit_x is None and bandit_y is None:
        # Choix aléatoire du type de bandit pour la première apparition
        if random.choice([True, False]):  # 50% de chance pour chaque
            bandit_x, bandit_y = random.choice(window_positions)
            current_bandit_image = random.choice([bandit_window])
        else:
            bandit_x = random.random() * (screeenWidth - bandit.get_width())
            bandit_y = 500  # Niveau du trottoir
            current_bandit_image = bandit
        bandit_visible = True

    if bandit_visible:
        screen.blit(current_bandit_image, (bandit_x - point_S_x, bandit_y - point_S_y))
        if bandit_x < point_S_x + dead_zone_left:
            affichage_gauche = True
            affichage_droite = False
        elif bandit_x > point_S_x + dead_zone_right:
            affichage_droite = True
            affichage_gauche = False
        else:
            affichage_gauche = False
            affichage_droite = False

    if affichage_gauche:
        screen.blit(fleche_gauche, (10, screenHeight // 2))
    if affichage_droite:
        screen.blit(fleche_droite, (screeenWidth - 10 - fleche_droite.get_width(), screenHeight // 2))

    screen.blit(viseur, (point_V_x, point_V_y))

    # Dessiner l'image "bang.png" si la touche ESPACE est pressée
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and bullet_count > 0:
        screen.blit(bang, (point_V_x + 10, point_V_y + 10))

    pygame.display.flip()

    # Apparition du bandit après un certain délai après la mort du précédent
    if bandit_timer is not None and pygame.time.get_ticks() - bandit_timer >= 3000:
        if random.choice([True, False]):  # Alternance des types de bandits après chaque mort
            bandit_x, bandit_y = random.choice(window_positions)
            current_bandit_image = random.choice([bandit_window])
        else:
            bandit_x = random.random() * (screeenWidth - bandit.get_width())
            bandit_y = 500  # Niveau du trottoir
            current_bandit_image = bandit
        bandit_visible = True
        bandit_timer = None  # Réinitialiser le timer

    # Affichage du score
    score_text = f'Score: {score}'

    Fond(screen, score_text, score_font, WHITE, screeenWidth - 160, screenHeight - 50)

    # Affichage des balles
    screen.blit(bullet, (screeenWidth - bullet.get_width() - 10, 10))
    bullet_text = police.render(str(bullet_count) + ' x', True, BLACK)
    bullet_rect = bullet_text.get_rect()
    bullet_rect.topright = (screeenWidth - bullet.get_width() - 20, 20)
    screen.blit(bullet_text, bullet_rect)

    if score >= 100:  # Vérifier si le score atteint 100
        Victoire(screen)
        done = True

    # Mise à jour de l'écran
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()