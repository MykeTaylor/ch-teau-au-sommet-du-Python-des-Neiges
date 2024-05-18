"""
Petit escape game
Auteur: MYKE TAYLOR
Date: 14 mai 2024
petit jeu d'escape game dans lequel l'utilisateur
doit sortir d'un labyrinthe tout en resolvant quelque
enigme
"""
from turtle import *   # module pour linterface graphique
from CONFIGS import *  # Module contenant les constante


def lire_matrice(fichier):
    """
    recuperation du plan à tracer dans un fichier txt
    et retour des differentes cases du plan
    :param fichier: fichier contenant le plan à tracer
    :return: matrice contenant les cases du plan
    """

    with open(fichier, 'r', encoding='utf-8') as plan:  # ouverture du fichier
        recup_plan = plan.read().split('\n')    # stockage des elements du fichiers dans une variable
        matrice = [[int(j) for j in i if j != " "] for i in recup_plan]     # matrice contenant chaque ligne du fichier
    return matrice


def calculer_pas(matrice):
    """
    calcul de la dimension à donner aux cases
    :param matrice: contenant les cases du plan
    :return: dimention des cases
    """

    nbre_ligne = len(matrice)   # recuperation du nombre de liste dans la matrice
    nbre_col = len(matrice[0])  # recuperation du nombre d'element dans la premiere liste de la matrice
    largeur_plan = abs(ZONE_PLAN_MINI[0]) + abs(ZONE_PLAN_MAXI[0])
    hauteur_plan = abs(ZONE_PLAN_MINI[1]) + abs(ZONE_PLAN_MAXI[1])
    if (hauteur_plan / nbre_ligne) <= (largeur_plan / nbre_col):   # verif de la plus petite valeur possible pour le pas
        pas = (hauteur_plan / nbre_ligne)
    else:
        pas = (largeur_plan / nbre_col)
    return pas


def coordonnees(case, pas):
    """
    calcule les coordonnées en pixels turtle du coin inférieur gauche
    d’une case définie par ses coordonnées (numéros de ligne et de colonne)
    :param case: represente les coordonnées d'une cases
    :param pas: reprensete la dimenssion d'une case
    :return: coordonnée en pixel turtle
    """

    val_vertical = ZONE_PLAN_MAXI[1] - (case[0] * pas)  # valeur pixel turtle de la case sur l'axe vertical
    val_horizontal = ZONE_PLAN_MINI[0] + (case[1] * pas)    # valeur pixel turtle de la case sur l'axe horizontal
    coord_tutle = (val_horizontal, val_vertical)  # coordonnée en pixel turtle d'une case
    return coord_tutle


def tracer_carre(dimension):
    """
    trace un carrer de coté = dimension à l'aide de turtle
    :param dimension: dimension du carre à tracer
    """
    for i in range(4):
        fd(dimension)   # avance le turtle
        left(90)   # inclinaison du turtle de 90° vers la droite


def tracer_case(case, couleur, pas):
    """
    traçage d'un carrer ayant une couleur bien definit
    à une position bien defini
    :param case: couple de coordonné en indice dans la matrice
    contenant le plan
    :param couleur: couleur du du carrer à tracer
    :param pas: dimension d'un coté du carrer
    """
    speed(0)     # augmente la vitesse du traçage du labyrinthe
    coordonne_turtle = coordonnees(case, pas)   # transforme les données de case en coodonné tutle
    teleport(coordonne_turtle[0], coordonne_turtle[1])  # positionnement du turtle au coordonné indiquer
    begin_fill()
    color(couleur[0], couleur[1])
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
            couleur = (COULEURS[0], COULEURS[matrice[i][j]])
            tracer_case((i, j), couleur, pas)


def position_centre_carrer(pos_pixel_turtle):
    """
    calcul le centre entre 2 points (cases) afin de positionner le
    personnage au centre du carrer
    :param pos_pixel_turtle:  position( pixel turtle) du personnge
    :return: centre du carrer
    """
    x = (pos_pixel_turtle[0] + (pos_pixel_turtle[0] + pas)) / 2
    y = (pos_pixel_turtle[1] + (pos_pixel_turtle[1] + pas)) / 2
    centre = (x, y)
    return centre


def deplacer_gauche():
    """
    deplacer le personnage sur la gauche
    :return:
    """
    global matrice
    global position
    onkeypress(None, "Left")
    verif_matrice = matrice[position[0]][position[1]-1]  # recupertion de la valeur dans la case a gauche du personnage
    if verif_matrice in [0, 2, 4]:  # verifi si cette valeur
        tracer_case(position, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        position = (position[0], position[1]-1)  # recupere la case de destination du personnage
        position_personage = position_centre_carrer(coordonnees(position, pas))  # position turtle du centre de la destination
        teleport(position_personage[0], position_personage[1])  # positionne le turtle à la destination
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE) # redessine le personnage
    onkeypress(deplacer_gauche, "Left")


def deplacer_bas():
    """
    deplacer le personnage sur la case en dessous
    :return:
    """
    global matrice
    global position
    onkeypress(None, "Down")
    verif_matrice = matrice[position[0]+1][position[1]]  # recuperation de la valeur dans la case en bas du personnage
    if verif_matrice in [0, 2, 4]:  # verifi si cette valeur
        tracer_case(position, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        position = (position[0]+1, position[1])
        position_personage = position_centre_carrer(coordonnees(position, pas))
        teleport(position_personage[0], position_personage[1])
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)
    onkeypress(deplacer_bas, "Down")


def deplacer_droite():
    """
    deplacer le personnage sur la case à droite
    :return:
    """
    global matrice
    global position
    onkeypress(None, "Right")
    verif_matrice = matrice[position[0]][position[1]+1]  # recupertion de la valeur dans la case a droite du personnage
    if verif_matrice in [0, 2, 4]:  # verifi si cette valeur
        tracer_case(position, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        position = (position[0], position[1]+1)
        position_personage = position_centre_carrer(coordonnees(position, pas))
        teleport(position_personage[0], position_personage[1])
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)
    onkeypress(deplacer_droite, "Right")


def deplacer_haut():
    """
    deplacer le personnage sur la case au dessus
    :return:
    """
    global matrice
    global position
    onkeypress(None, "Up")
    verif_matrice = matrice[position[0]-1][position[1]]  # recupertion de la valeur dans la case au dessus du personnage
    if verif_matrice in [0, 2, 4]:  # verifi si cette valeur
        tracer_case(position, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        position = (position[0]-1, position[1])
        position_personage = position_centre_carrer(coordonnees(position, pas))
        teleport(position_personage[0], position_personage[1])
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)
    onkeypress(deplacer_haut, "Up")


ht()    # rendre la turtle invisible
matrice = lire_matrice(fichier_plan)  # recuperation de la matrice
afficher_plan(matrice)  # appel de la fonction pour affichage du plan
pas = calculer_pas(matrice)  # recuperation du pas (dimenssion)
position = POSITION_DEPART  # cases de depart du personnage
depart_pixel_turtle = position_centre_carrer(coordonnees(position, pas))   # position de depart en pixel turtle du joueur
teleport(depart_pixel_turtle[0], depart_pixel_turtle[1])
dot((calculer_pas(matrice)*RATIO_PERSONNAGE), COULEUR_PERSONNAGE)
listen()
onkeypress(deplacer_bas, "Down")
onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
onkeypress(deplacer_droite, "Right")
onkeypress(deplacer_haut, "Up")
mainloop()
