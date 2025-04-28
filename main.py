

import pygame
import sys
import time
from random import randint
from pygame.locals import *

pygame.init()

LARGEUR = 640
HAUTEUR = 480

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Snake')

###############################################################################
 
# Couleurs
GRIS = (221, 221, 221)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
BLEUC = (112, 193, 237)
BLEUF = (18, 98, 141)

# (1, 2, 3, 4) = ('Bas', 'Haut', 'Droite', 'Gauche')
DIRECTION = 0

COTE = 10

FOOD = 1

###############################################################################
 
class Snake(object):
    def __init__(self):
        self.corps = BLEUC
        self.tete = BLEUF
        self.serpent = [{'rect':pygame.Rect(LARGEUR/2, HAUTEUR/2,
                COTE, COTE), 'color':self.tete, 'dire':0}}]
        self.score = 0
    def addblock(self, n):
        # ajoute n carrés à droite de la queue du serpent
        i = 0
        while i < n:
            # On utilise les valeurs de la queue pour définir le carré
            Y = self.serpent[len(self.serpent)-1]['rect'].top - COTE - 1
            X = self.serpent[len(self.serpent)-1]['rect'].left          
            DIRE = self.serpent[len(self.serpent)-1]['dire']
             
            self.serpent.append({'rect':pygame.Rect(X, Y, COTE, COTE),
                                 'color':self.corps, 'dire':DIRE})
            i+=1
     
    def moove(self):
        # On supprime la queue...
        del self.serpent[len(self.serpent)-1]
         
        # ...puis on définit une nouvelle tête à partir de l'ancienne
        Y = self.serpent[0]['rect'].top
        X = self.serpent[0]['rect'].left
         
        if DIRECTION == 1:
            Y += (COTE + 1)
        if DIRECTION == 2:
            Y -= (COTE + 1)            
        if DIRECTION == 3:
            X += (COTE + 1)
        if DIRECTION == 4:
            X -= (COTE + 1)
             
        self.serpent = [{'rect':pygame.Rect(X, Y, COTE, COTE),
                 'color':self.tete, 'dire':DIRECTION}] + self.serpent
        self.serpent[1]['color'] = self.corps
         
def nourriture():
    # -10 pour que le carré soit toujours affiché en entier
    X = randint(0, LARGEUR-10)
    Y = randint(0, HAUTEUR-10)
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    global food
    food = {'rect':pygame.Rect(X, Y, 10, 10), 'color':color}
                     
###############################################################################
 
sn = Snake()
sn.addblock(2)
nourriture()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
             
        if event.type == KEYDOWN:
             
            # définit la direction (et on empêche les demi-tours)
            if event.key == K_DOWN and DIRECTION != 2: DIRECTION = 1
            if event.key == K_UP and DIRECTION != 1: DIRECTION = 2
            if event.key == K_RIGHT and DIRECTION != 4: DIRECTION = 3
            if event.key == K_LEFT and DIRECTION != 3: DIRECTION = 4
                 
            # arrêt 
            if event.key == K_RSHIFT: DIRECTION = 0
            #if event.key == K_SPACE:
            #if event.key ==K_RCTRL:
      
    # fond de la fenêtre      
    fenetre.fill(GRIS)
     
    # s'il y a ordre de déplacement on appelle la méthode moove()
    # mais on attend 0.05 secondes pour obtenir une vitesse stable et jouable
    if DIRECTION:
        time.sleep(0.05)
        sn.moove()
     
    # si la tête touche un bord on la fait passer de l'autre côté   
    if sn.serpent[0]['rect'].top >= HAUTEUR: sn.serpent[0]['rect'].top = 1
    if sn.serpent[0]['rect'].top <= 0: sn.serpent[0]['rect'].top = HAUTEUR
    if sn.serpent[0]['rect'].left >= LARGEUR: sn.serpent[0]['rect'].left = 1
    if sn.serpent[0]['rect'].left <= 0: sn.serpent[0]['rect'].left = LARGEUR
     
    # on affiche le serpent   
    for carre in sn.serpent:
        pygame.draw.rect(fenetre, carre['color'], carre['rect'])
         
    # et la nourriture
    pygame.draw.rect(fenetre, food['color'], food['rect'])
     
    # on regarde si la tête du serpent est en contact avec la nourriture...
    # si oui, on génère une nouvelle nourriture
    # puis on ajoute un point au score et un carré au serpent
    if sn.serpent[0]['rect'].left >= food['rect'].left:
        if sn.serpent[0]['rect'].left <= food['rect'].right:
            if sn.serpent[0]['rect'].top >= food['rect'].top:
                if sn.serpent[0]['rect'].top <= food['rect'].bottom:
                    sn.score += 1
                    sn.addblock(1)
                    nourriture()
     
    if sn.serpent[0]['rect'].right >= food['rect'].left:
        if sn.serpent[0]['rect'].right <= food['rect'].right:
            if sn.serpent[0]['rect'].bottom <= food['rect'].bottom:
                if sn.serpent[0]['rect'].bottom >= food['rect'].top:
                    sn.score += 1
                    sn.addblock(1)
                    nourriture()
         
    # affiche la taille du serpent, le score et la position de la tête
    police = pygame.font.Font(None, 14)
    tvit = police.render('Taille : {} ; Score : {}'.
                format(len(sn.serpent), sn.score),1,NOIR)
    tpos = police.render('Position : {}'.format((sn.serpent[0]['rect'].left,
                sn.serpent[0]['rect'].top)),1,NOIR)
    fenetre.blit(tvit,(10,10))
    fenetre.blit(tpos,(10,24))
             
    pygame.display.update()