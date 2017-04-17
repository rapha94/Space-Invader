# Importation de la librairie pygame & des constantes pygames
import pygame
from pygame.locals import *
import random
import time  


# Déclaration  de mes variables de dimention de ma fenêtre & de ma fréquence.
WIDTH = 650
HEIGHT = 750
FPS = 300

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 99, 71)
# Initialisation des modules de pygame
pygame.init()
pygame.mixer.init()

# Création de ma fenêtre & insertion d'une image de fond
window = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("Space.jpg").convert()
window.blit(background, (0, 0))  #  On colle le fond sur la surface vide qu'est fenêtre. (0,0) étant le point de collage.

# Association de mes fichiers images à mes variables images.
joueur_img = pygame.image.load("fighter.png").convert_alpha()
mob_img = pygame.image.load("Meteor.png").convert_alpha()
missile_img = pygame.image.load("GreenLaser.png").convert_alpha()

# Association de mes fichiers audios à mes variables audio & réglage du volume.
missile_bruit = pygame.mixer.Sound("Tire.wav")
mob_bruit = pygame.mixer.Sound("Explosion.wav")
crash_bruit = pygame.mixer.Sound("Crash.wav")

missile_bruit.set_volume(0.05)
mob_bruit.set_volume(0.05)
crash_bruit.set_volume(0.2)

# Titre de ma fenêtre et création de ma variable Horloge
pygame.display.set_caption("Asteroid Cloud")
clock = pygame.time.Clock()









# Déclaration de mes fonctions

# Fonction pour rejouer
def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.QUIT]):
        if event.type == pygame.QUIT :
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                main()
            elif event.key == pygame.K_q:
                pygame.quit()
            else:
                main()
        return event.key

    return None

#  Déclaration de ma fonction qui affiche un message avec choix de ma police.
font_name = pygame.font.match_font("arial")


def draw_text(surf, text, size, x, y):  #   Fonction affichage text
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)  # TRUE active la fonction  ANTIALIAS (meilleur rendu)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


#   Déclaration de ma fonction Game OVER
def game_over():
    while replay_or_quit() == None:
        pygame.display.update()
        draw_text(window, str("GAME OVER! Pressez Q pour Quitter ou R pour Recommencer!"), 18, WIDTH/2, HEIGHT/2)
        clock.tick()


#  Déclaration de la fonction qui génére des astéroides
def create_mob(NB):

    for i in range(NB):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)


#  Déclaration de mes class (attributs & méthodes)

# Classe de mon joueur principal
class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        # Déclaration des attributs de mon joueur
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image = joueur_img
        self.rect = self.image.get_rect()
        self.radius = 23
        #  pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        #  Mise à jour de mon joueur
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()         # Mouvements de mon joueur
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
                                                    # Cadre de déplacement de mon joueur
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    # Déclaration de ma méthode missile pour mon joueur (qui envoie des missiles donc crée les objets missiles )
    def tire(self):
        missile = Missile(self.rect.centerx, self.rect.top)
        all_sprites.add(missile)
        missiles.add(missile)
        missile_bruit.play()


# Class de mes astéroides.
class Mob(pygame.sprite.Sprite):
    #   Attributs de mes objets astéroides
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (40, 40))
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image,BLUE,self.rect.center,self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(mini, maxi)
        self.speedx = random.randrange(-3, 3)

    #   Mise à jour de mes astéroides
    def update(self, mini, maxi):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(mini, maxi)


# Classe de missiles
class Missile(pygame.sprite.Sprite):
    # Attributs de mes objets missiles
    def __init__(self, x, y):
        pygame.sprite.Sprite. __init__ (self)
        self.image = pygame.transform.scale(missile_img, (5, 20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    # Mise à jour de mes missiles
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Création de mes groupes de sprites
all_sprites = pygame.sprite.Group()  # all_sprite contiendra tous les objets afin de tous les afficher d'un seul coup.
missiles = pygame.sprite.Group()     # missiles contiendra tous mes objets missiles afin de gérer leurs comportements.
mobs = pygame.sprite.Group()         # mobs (astéroides) contiendra tous mes objets mobs (astéroides)afin de gérer leurs comportement.

joueur = Joueur()                   # Je créee un objet Joueur (mon joueur principal)
all_sprites.add(joueur)
#   J'intégre mon objet dans le groupe.
mini = 1
maxi = 8
#   Création de mes astéroides.
create_mob(10)


# Déclaration de ma fonction principale
def main():
    # Initialisation de mes valeures
    score = 0
    mini = 1
    maxi = 8
    joueur.rect.centerx = WIDTH/2
    joueur.rect.bottom = HEIGHT-10

    # Boucle de jeu
    running = True
    while running:
        #  Définition de la fréquence de lecture de ma boucle.
        clock.tick(FPS)
        # Gestion des événement extérieurs
        for event in pygame.event.get():
            # Vérification si la commande de fermeture de fenêtre a été activée.
            if event.type == pygame.QUIT:
                running = False
            # Vérification si la commande de lancement de missile a été activée.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    joueur.tire()

        # Mise à jours de  mes objets.

        #all_sprites.update(mini, maxi)
        joueur.update()
        mobs.update(mini, maxi)
        missiles.update()

        #  Collision entre un missile et un astéroide.
        hits = pygame.sprite.groupcollide(mobs, missiles, True, True)
        for hit in hits:
            score +=1           #w  A chaque fois que je détruit un astéroides,j'incrémente mon score de 1
            mob_bruit.play()    # Bruitage de la déstruction de mon astéroide.
            create_mob(1)       #  A chaque fois que je détruit un astéroide, j'en crée un nouveau

        #   Collision entre mon avion et un astéroide (CRASH)
        hits = pygame.sprite.spritecollide(joueur, mobs, True, pygame.sprite.collide_circle)
        if hits:
            crash_bruit.play()
            game_over()

        #  Augmentation de la difficulté
        if score > 20 and score < 40:
            mini = 2
            maxi = 10
        elif score > 40 and score < 60:
            mini = 6
            maxi = 12
        elif score > 60 and score < 80:
            mini = 8
            maxi = 14
        elif score > 80 and score < 90:
            mini = 10
            maxi = 16
        elif score > 90 and score < 100:

            mini = 12
            maxi = 18
        elif score > 100 and score < 110:
            mini = 15
            maxi = 20
        elif score > 110 and score < 120:
            mini = 17
            maxi = 23
        elif score > 120 and score < 130:
            mini = 20
            maxi = 26
        elif score > 130 and score < 140:
            mini = 26
            maxi = 30
        elif score > 140 and score < 150:
            mini = 30
            maxi = 35
        elif score > 140 and score < 150:
            mini = 30
            maxi = 35
        elif score > 150:
            mini = 35
            maxi = 45

        #  Affichage de mes différents éléments
        window.blit(background, (0, 0))
        all_sprites.draw(window)
        draw_text(window, str(score), 58, WIDTH/2, 20)

        #  Une fois l'affichage éffectué on "tourne le tableau" afin d'afficher plus rapidement (double buffering )
        pygame.display.flip()

main()
pygame.quit()

