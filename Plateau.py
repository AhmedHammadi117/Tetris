#Lina Tritar , Hammadi Ahmed

import random
from math import *
from code import Point, Tetramino
from interface import *

#On a crée un objet tetramino à partir de 4 points (0,0) initiales pour pouvoir faire les modifications
p = Point(0, 0)
p1 = Point(0, 0)
p2 = Point(0, 0)
p3 = Point(0, 0)
l = [p, p1, p2, p3]
t = Tetramino(l,'noir')

class Plateau:
    
    def __init__(self, ecran):
        
        self.ecran = ecran
        self.grille_largeur = 15
        self.grille_hauteur = 17
        
        #Création d'une matrice des positions de meme dimmension que l'ecran initialisé par des "None"
        self.grille = [[None] * self.grille_largeur for _ in range(self.grille_hauteur)]
        #Création d'une matrice de couleur de meme dimmension que l'ecran initialisé par des "None"
        self.couleur_grille = [[None] * self.grille_largeur for _ in range(self.grille_hauteur)]
        
        
        self.piece_actuelle = self.generer_nv_piece()# création d'un objet tetramino aléatoire
        self.piece_suivante = None #Intialise la 2ème piece( c'est la piece qui s'affiche quand on ecrase deux lignes avec une seule piece)à "None" 
        #Pour la piece suivante, None represente l'inactivité
        self.temporisation = 20  # Delay in milliseconds
        self.compteur_temps = 0
        self.score=0

# Création d'une piece tetramino avec sa propre forme et couleur aléatoirement
    def generer_nv_piece(self):
        formes = [t.Té(),t.carre(),t.lamda(),t.gama(),t.barre(),t.biais(),t.biais_inver()]
        couleurs=['mauve', 'jaune', 'orange', 'bleu', 'cyan', 'rouge', 'vert']
        index=random.randint(0,len(formes)-1)
        piece=Tetramino(formes[index],couleurs[index])
        piece.translater(piece.vect_posi())#Affichage de la piece au milieu de l'ecran en rajoutant le vect_posi
        return piece

#La methode dessiner_grille fait l'affichage de la grille
    def dessiner_gille(self):
        for y in range(self.grille_hauteur):
            for x in range(self.grille_largeur):
                if self.couleur_grille[y][x] is not None:
                    self.ecran.write(" ", x, y, bgcolor=self.ecran.COULEUR[self.couleur_grille[y][x]])
                    # Si la position est occupé on dessine le point avec sa couleur dans la couleur_grille
                else:
                    self.ecran.write(" ", x, y, bgcolor=self.ecran.COULEUR['blanc'])

    def dessiner_piece(self,piece):
        for point in piece.image():
            x, y = point.x, point.y
            self.ecran.write(" ", x, y, bgcolor=self.ecran.COULEUR[self.piece_actuelle.couleur])

    def piece_tombe(self):
        if self.piece_suivante == None:#Si il y a absence de piece suivante on verifie seulement la piece actuelle
            for point in self.piece_actuelle.image():
                x, y = int(point.x), int(point.y)
                if y == self.grille_hauteur - 1 or (self.grille[int(y) + 1][int(x)] is not None):
                #Vérifie si la piece est à la derniere ligne et teste la collision
                    return True
            return False
        else:# On verifie les deux pieces:actuelle et suivante (la piece suivante est active)
            t=False
            for point in self.piece_actuelle.image():
                x, y = int(point.x), int(point.y)
                if y == self.grille_hauteur - 1 or (self.grille[int(y) + 1][int(x)] is not None):
                #Vérifie si la piece est à la derniere ligne et teste la collision
                    t=True
            for point in self.piece_suivante.image():
                x, y = int(point.x), int(point.y)
                if y == self.grille_hauteur - 1 or (self.grille[int(y) + 1][int(x)] is not None):
                #Vérifie si la piece est à la derniere ligne et teste la collision
                    t=True
            
            return t
        
    def piece_touche_bord(self, dx):
        if self.piece_suivante == None:
            for point in self.piece_actuelle.image():
                x, y = int(point.x) + dx, int(point.y)
                if x < 0 or x >= self.grille_largeur or (self.grille[y][x] is not None) :
                #Vérifie si la piece sort de la grille et ne fusionne pas avec une autre piece
                    return True
            return False
        else:
            t=False
            for point in self.piece_actuelle.image():
                x, y = int(point.x) + dx, int(point.y)
                if x < 0 or x >= self.grille_largeur or (self.grille[y][x] is not None) :
                #Vérifie si la piece actuelle sort de la grille et  ne fusionne pas avec une autre piece
                    t=True
            for point in self.piece_suivante.image():
                x, y = int(point.x) + dx, int(point.y)
                if x < 0 or x >= self.grille_largeur or (self.grille[y][x] is not None) :
                #Vérifie si la piece suivante sort de la grille et ne fusionne pas avec une autre piece
                    t=True
            return t
                 

    def translater_piece_bas(self):
        if self.piece_suivante == None :
            if not self.piece_tombe():
                self.piece_actuelle.translater(Point(0, 1))
            else:
                self.piece_fixe()
                self.supprimer_lignes()#Verifie la possibilité d'ecrasement d'une ligne
                self.piece_actuelle = self.generer_nv_piece()#Crée une autre piece
        else:# Applique la translation en bas sur les deux pieces en meme temps 
            if not self.piece_tombe():
                self.piece_actuelle.translater(Point(0, 1))
                self.piece_suivante.translater(Point(0, 1))
                
            else:
                self.piece_fixe()
                self.supprimer_lignes()#Verifie la possibilite d'ecrasement d'une ligne
                self.piece_actuelle = self.generer_nv_piece()#Crée une autre piece pour la piece actuelle
                self.piece_suivante=None #La piece suivante reprend la valeur de None pour ne pas afficher à chaque fois une nouvelle piece
            

    def translater_piece_gauche(self):
        if not self.piece_touche_bord(-1):
            self.piece_actuelle.translater(Point(-1, 0))

    def translater_piece_droite(self):
        if not self.piece_touche_bord(1):
            self.piece_actuelle.translater(Point(1, 0))

    def rotation_piece(self):
        rotated_piece = self.piece_actuelle.clonage()#Création d'une copie de la piece actuelle
        rotated_piece.tourner()#On fait tourner la copie
        for point in rotated_piece.image():
            x, y = int(round(point.x)),int(round(point.y))
            if x < 0 or x >= self.grille_largeur or y < 0 or y >= self.grille_hauteur or (self.grille[y][x] is not None):
                #Teste si la copie sort de l'ecran aprés la rotation
                return
            
        self.piece_actuelle = rotated_piece
        
#Stockage des positions et des couleurs des pieces dans la grille
    def piece_fixe(self):
        for point in self.piece_actuelle.image():
            self.grille[int(point.y)][int(point.x)] = point
            self.couleur_grille[int(point.y)][int(point.x)]=self.piece_actuelle.couleur
        
        if self.piece_suivante != None:#La piece suivante est active , on stocke les points de la piece suivante dans la grille
            for point in self.piece_suivante.image():
                self.grille[int(point.y)][int(point.x)] = point
                self.couleur_grille[int(point.y)][int(point.x)]=self.piece_suivante.couleur

#Vérifie si la ligne est complete si c'est le cas on l'ecrase et on l'ajoute dans la liste 
    def supprimer_lignes(self):
        lines_to_clear = []
        for y in range(self.grille_hauteur):
            if all(self.grille[y]):
                lines_to_clear.append(y)
        for line in lines_to_clear:
            del self.grille[line]
            self.grille.insert(0, [None] * self.grille_largeur)
            del self.couleur_grille[line]
            self.couleur_grille.insert(0, [None] * self.grille_largeur)

#Compte le score selon le nombre de lignes ecrasee        
        if len(lines_to_clear) == 1:
            self.score += 40
        elif len(lines_to_clear) == 2:
            self.score += 100
            self.piece_suivante=self.generer_nv_piece() #La condition est vérifiée ,la piece suivante prend une nouvelle piece
            self.piece_suivante.translater(Point(-4,0))#On fait deplacer la piece suivante pour que ça soit pas en collision avec la piece actuelle
            
        elif len(lines_to_clear) == 3:
            self.score += 300
        elif len(lines_to_clear) == 4:
            self.score += 1200
  
#Affichage du score 
    def afficher_score(self):
        for i in range (15):
            self.ecran.write(" ", i, 0, bgcolor=self.ecran.COULEUR['noir'])
        self.ecran.write(f"Score: {self.score}", 0, 0, fgcolor=self.ecran.COULEUR['rouge'], bgcolor=self.ecran.COULEUR['noir'])
    
#Commande du déplacement ou de la rotation selon les touches.
    def lire_touche(self):
        touche = self.ecran.lire_touche()
        if touche == KST.DROITE:
            self.translater_piece_droite()
        elif touche == KST.GAUCHE:
            self.translater_piece_gauche()
        elif touche == KST.BAS:
            self.translater_piece_bas()
        elif touche == KST.HAUT:
            self.rotation_piece()
        elif touche == KST.ESPACE:# À chaque appui sur la touche espace, on alterne le contrôle entre les deux pièces.
            copie=self.piece_actuelle
            self.piece_actuelle=self.piece_suivante
            self.piece_suivante=copie
            

    def verifier_gameover(self):
        gameover= True
        if self.grille[1][7] is None:
            gameover = False
        return gameover
    
    
    def jouer(self):
        while True:
            self.ecran.ecran.fill(self.ecran.COULEUR['blanc'])
            self.lire_touche()
            if self.compteur_temps % self.temporisation == 0: #On descend à chaque temporisation indiqué.
                self.translater_piece_bas()
            
            self.dessiner_gille()
            
            if self.piece_suivante == None:#Si la piece suivante est inactive , on affiche seulement la piece actuelle.
                self.dessiner_piece(self.piece_actuelle) 
            else:#On affiche les deux pieces.
                self.dessiner_piece(self.piece_actuelle)
                self.dessiner_piece(self.piece_suivante)
            self.afficher_score()
            
            if self.verifier_gameover():
                self.ecran.write("Game Over", 3, 7, fgcolor=self.ecran.COULEUR['rouge'], bgcolor=self.ecran.COULEUR['noir'])
                self.ecran.mise_a_jour()
                self.ecran.pause(2000)  # Pause de 2 secondes avant de quitter.
                break
    
            
            self.ecran.mise_a_jour()
            self.compteur_temps += 1
            
            if self.compteur_temps >= 100:
                self.compteur_temps = 0
            self.ecran.pause(40)
           
