"""
Petit escape game
Auteur: MYKE TAYLOR
Date: 14 mai 2024
petit jeu d'escape game dans lequel l'utilisateur
doit sortir d'un labyrinthe tout en resolvant quelque
enigme
"""
from turtle import *    # module pour linterface graphique
from CONFIGS import *  # Module contenant les constante

def lire_matrice(fichier):
    '''
    recuperation du plan à tracer dans un fichier txt
    et retour des differentes cases du plan
    :param fichier: fichier contenant le plan à tracer
    :return: matrice contenant les cases du plan
    '''

    with open(fichier, 'r', encoding='utf-8') as plan:  # ouverture du fichier
        recup_plan = plan.read().split('\n')    # stockage des elements du fichiers dans une variable
        matrice = [[int(j) for j in i if j != " "] for i in recup_plan]     # matrice contenant chaque ligne du fichier sous forme de liste
    return matrice

def calculer_pas(matrice):
    """
    calcul de la dimension à donner aux cases
    :param matrice: contenant les cases du plan
    :return: dimention des cases
    """
    pas = 0  # initialisation de la dimension des cases à 0
    nbre_ligne = len(matrice)   # recuperation du nombre de liste dans la matrice
    nbre_col = len(matrice[0])  # recuperation du nombre d'element dans la premiere liste de la matrice
    nbre_case = nbre_col * nbre_ligne
    largeur_plan = abs(ZONE_PLAN_MINI[0]) + abs(ZONE_PLAN_MAXI[0])
    hauteur_plan = abs(ZONE_PLAN_MINI[1]) + abs(ZONE_PLAN_MAXI[1])
    if (hauteur_plan / nbre_ligne) <= (largeur_plan / nbre_col):    # verif de la plus petite valeur possible pour le pas
        pas = (hauteur_plan / nbre_ligne)
    else:
        pas = (largeur_plan / nbre_col)
    return pas

def coordonnees(case, pas):
    '''
    calcule les coordonnées en pixels turtle du coin inférieur gauche
    d’une case définie par ses coordonnées (numéros de ligne et de colonne)
    :param case: represente les coordonnées d'une cases
    :param pas: reprensete la dimenssion d'une case
    :return: coordonnée en pixel turtle
    '''
    val_vertical = 0    # valeur pixel turtle de la case sur l'axe vertical initialisé a 0
    val_horizontal = 0  # valeur pixel turtle de la case sur l'axe horizontal initialisé a 0
    val_vertical = ZONE_PLAN_MAXI[1] - (case[0] * pas)
    val_horizontal = ZONE_PLAN_MINI[0] + (case[1] * pas)
    coord_tutle = ( val_horizontal,val_vertical)  # coordonnée en pixel turtle d'une case
    return coord_tutle

def  tracer_carre(dimension):
    """
    trace un carrer de coté = dimension à l'aide de turtle
    :param dimension: dimension du carre à tracer
    """
    for i in range(4):
        fd(dimension)
        right(90)

def tracer_case(case, couleur, pas):
    """
    traçage d'un carrer ayant une couleur bien definit
    à une position bien defini
    :param case: couple de coordonné en indice dans la matrice
    contenant le plan
    :param couleur: couleur du du carrer à tracer
    :param pas: dimension d'un coté du carrer
    """
    speed((0))     # augmente la vitesse du traçage du labyrinthe
    coordonne_turtle = coordonnees(case, pas)   # transforme les données de case en coodonné tutle
    teleport(coordonne_turtle[0], coordonne_turtle[1])  # positionnement du turtle au coordonné indiquer
    begin_fill()
    color(couleur[0],couleur[1])
    tracer_carre(pas)   # traçage du carrer
    end_fill()

def afficher_plan(matrice):
    """

    :param matrice:
    :return:
    """
    pas = calculer_pas(matrice)
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            couleur = (COULEURS[0],COULEURS[matrice[i][j]])
            tracer_case((i,j), couleur, pas)
    mainloop()

Matrice= lire_matrice(fichier_plan)
afficher_plan(Matrice)
