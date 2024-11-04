#Hammadi Ahmed, Tritar Lina
import pygame
from pygame.locals import *
import random 
from Plateau import *


class KST:
    __slots__ = ()

    HAUT = 0
    DROITE = 1
    BAS = 2
    GAUCHE = 3
    ESPACE = 4

class Interface:
    def __init__(self, dim_x, dim_y, titre):
        self.clock = pygame.time.Clock()
        self.taille_fonte_y = 40
        pygame.init()
        if not pygame.font.get_init():
            print("Désolé, les fontes de caractères sont absentes, je ne peux démarrer")
            quit()
        self.font = pygame.font.SysFont("Courier, Monospace", self.taille_fonte_y)
        self.taille_fonte_x = self.font.size('M')[0]
        self.ecran = pygame.display.set_mode((dim_x * self.taille_fonte_x, dim_y * self.taille_fonte_y))
        pygame.display.set_caption(titre)
        self.COULEUR = {
            'vert': (11, 240, 11),
            'rouge': (213, 11, 11),
            'orange': (213, 180, 11),
            'jaune': (213, 213, 11),
            'bleu': (40, 40, 240),
            'blanc': (255, 255, 255),
            'gris': (210, 210, 210),
            'noir': (0, 0, 0),
            'cyan':(135,206,250),
            'mauve':(238,130,238)
        }
        self.NOM_COULEUR = list(self.COULEUR.keys())

    def curseur(self, x, y):
        return (x * self.taille_fonte_x, y * self.taille_fonte_y)

    def write(self, texte, x, y, fgcolor=(255,255,255), bgcolor=(0,0,0)):
        texte = self.font.render(texte, True, pygame.Color(fgcolor), pygame.Color(bgcolor))
        self.ecran.blit(texte, self.curseur(x, y))

    def pause(self, tempo):
        self.clock.tick(tempo)

    def mise_a_jour(self):
        pygame.display.flip()

    def lire_touche(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return KST.HAUT
                elif event.key == pygame.K_DOWN:
                    return KST.BAS
                elif event.key == pygame.K_LEFT:
                    return KST.GAUCHE
                elif event.key == pygame.K_RIGHT:
                    return KST.DROITE
                elif event.key == pygame.K_SPACE:
                    return KST.ESPACE
        return None

    def fermer(self):
        pygame.quit()

def main():
    ecran = Interface(15, 17, "Tetris")
    game = Plateau(ecran)
    game.jouer()

if __name__ == "__main__":
    main()


