#Hammadi Ahmed, Tritar Lina
from math import *
import random

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, autre):
        return self.x==autre.x and self.y==autre.y

    def __repr__(self):
        return '(' + str(self.x) + "," + str(self.y) + ")"

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

#La rotation d'un point à l'aide de la matrice de rotation
    def rotation_point(self, c):
        angl = radians(c)
        x = self.x
        y = self.y
        new_x = round(cos(angl)) * x + round(-sin(angl)) * y
        new_y = round(sin(angl)) * x + round(cos(angl)) * y
        return Point(int(new_x), int(new_y))


class Tetramino:

#Initailisation des 4 points dont le premier est le centre de rotation.  
    def __init__(self, lst, couleur):
        self.ctr_rot = lst[0]
        self.point2 = lst[1]
        self.point3 = lst[2]
        self.point4 = lst[3]
        self.couleur=couleur
        self.rotation = 0
       
    def __repr__(self):
        return str([self.ctr_rot, self.point2, self.point3, self.point4])

#Creation des 7 formes de Tetraminos. 
    def carre(self):
        self.point2 = self.ctr_rot + Point(0, 1)
        self.point3 = self.ctr_rot + Point(1, 1)
        self.point4 = self.ctr_rot + Point(1, 0)
        return [self.ctr_rot, self.point2, self.point3, self.point4]

    def Té(self):
        self.point2 = self.ctr_rot + Point(1, 0)
        self.point3 = self.ctr_rot + Point(-1, 0)
        self.point4 = self.ctr_rot + Point(0, 1)
        return [self.ctr_rot, self.point2, self.point3, self.point4]

    def gama(self):
        self.point2 = self.ctr_rot + Point(1, 0)
        self.point3 = self.ctr_rot + Point(-1, 0)
        self.point4 = self.ctr_rot + Point(-1, 1)
        return [self.ctr_rot, self.point2, self.point3, self.point4]

    def lamda(self):
        self.point2 = self.ctr_rot + Point(1, 0)
        self.point3 = self.ctr_rot + Point(-1, 0)
        self.point4 = self.ctr_rot + Point(1, 1)
        return [self.ctr_rot, self.point2, self.point3, self.point4]

    def biais(self):
        self.point2 = self.ctr_rot + Point(1, 0)
        self.point3 = self.ctr_rot + Point(0, -1)
        self.point4 = self.ctr_rot + Point(-1, -1)
        return [self.ctr_rot, self.point2, self.point3, self.point4]

    def biais_inver(self):
        self.point2 = self.ctr_rot + Point(-1, 0)
        self.point3 = self.ctr_rot + Point(0, -1)
        self.point4 = self.ctr_rot + Point(1, -1)
        return [self.ctr_rot, self.point2, self.point3, self.point4]

    def barre(self):
        self.point2 = self.ctr_rot + Point(-1, 0)
        self.point3 = self.ctr_rot + Point(1, 0)
        self.point4 = self.ctr_rot + Point(2, 0)
        return [self.ctr_rot, self.point2, self.point3, self.point4]

#vect_posi represente la position initiale du Tetramino sur l'ecran.
    def vect_posi(self):
        return Point(7,2)

#Translater: on ajoute à chaque point du tetramino un déplacement vect.
    def translater(self, vect):
        self.ctr_rot += vect
        self.point2 += vect
        self.point3 += vect
        self.point4 += vect
        
#Tourner:
        #Le centre de rotaion stocke le nombre de translations appliqueés.
        # list_init donne la forme initiale du tetramino.
        # La premiere condition teste si la forme est un carré , il fait pas de rotation.
        # On applique la rotation pour chaque point du tetramino à l'aide de la méthode rotation_point.
        # On stocke le nombre de rotation dans l'instance self.rotation .
    def tourner(self):
        list_init=[(self.ctr_rot - self.ctr_rot),(self.point2 - self.ctr_rot),(self.point3 - self.ctr_rot),(self.point4 - self.ctr_rot)]
        if list_init[0]==Point(0,0)and list_init[1]==Point(0, 1)and list_init[2]==Point(1, 1)and list_init[3]==Point(1, 0):
            return
        self.rotation=(self.rotation+90)%360
        self.point2 = self.ctr_rot + list_init[1].rotation_point(90)
        self.point3 = self.ctr_rot + list_init[2].rotation_point(90)
        self.point4 = self.ctr_rot + list_init[3].rotation_point(90)

# La methode image retourne la liste des 4 points du tetramino.
# On n'a pas rajoute le vecteur de position et de rotation dans la methode image car on les a utilisés dans la class plateau. 
    def image(self):
        points = [self.ctr_rot, self.point2, self.point3, self.point4]
        return points
    
#La methode clonage retoune une copie de l'objet tetramino.
    def clonage(self):
        lst_copie = [self.ctr_rot, self.point2, self.point3, self.point4]
        tetr_copie = Tetramino(lst_copie,self.couleur)
        return tetr_copie
    
    def couleur(self):
        return self.couleur

