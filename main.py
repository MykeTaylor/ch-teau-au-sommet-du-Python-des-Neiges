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
    à une case bien defini
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
    """
    global matrice
    global case
    global objet_recuperer
    global dict_objet
    case_mouvement = (case[0], case[1]-1)  # case situer a gauche (ligne , colonne)
    onkeypress(None, "Left")
    verif_matrice = matrice[case[0]][case[1]-1]  # recupertion de la valeur dans la case a gauche du personnage
    if verif_matrice in [0, 2, 4]:  # verification de  cette valeur
        tracer_case(case, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        case = case_mouvement  # recupere la case de destination du personnage
        position_personage = position_centre_carrer(coordonnees(case, pas))  # coordonne turtle du centre du carrer
        teleport(position_personage[0], position_personage[1])  # positionne le turtle au centre du carrer
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)     # redessine le personnage
        if verif_matrice == 4:
            ramasser_objet(matrice, case, objet_recuperer, dict_objet)
    elif verif_matrice == 3:
        case = poser_question(matrice, case, case_mouvement)
        position_personage = position_centre_carrer(coordonnees(case, pas))  # coordonne du centre du carrer
        teleport(position_personage[0], position_personage[1])  # positionne le turtle au centre du carrer
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)  # redessine le personnage
    onkeypress(deplacer_gauche, "Left")


def deplacer_bas():
    """
    deplacer le personnage sur la case en dessous
    """
    global matrice
    global case
    global objet_recuperer
    global dict_objet
    case_mouvement = (case[0]+1, case[1])
    onkeypress(None, "Down")
    verif_matrice = matrice[case[0]+1][case[1]]  # recuperation de la valeur dans la case en bas du personnage
    if verif_matrice in [0, 2, 4]:  # verification de  cette valeur
        tracer_case(case, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        case = case_mouvement
        position_personage = position_centre_carrer(coordonnees(case, pas))
        teleport(position_personage[0], position_personage[1])
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)
        if verif_matrice == 4:
            ramasser_objet(matrice, case, objet_recuperer, dict_objet)
    elif verif_matrice == 3:
        case = poser_question(matrice, case, case_mouvement)
        position_personage = position_centre_carrer(coordonnees(case, pas))  # coordonne du centre du carrer
        teleport(position_personage[0], position_personage[1])  # positionne le turtle au centre du carrer
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)  # redessine le personnage
    onkeypress(deplacer_bas, "Down")


def deplacer_droite():
    """
    deplacer le personnage sur la case à droite

    """
    global matrice
    global case
    global objet_recuperer
    global dict_objet
    case_mouvement = case[0], case[1]+1
    onkeypress(None, "Right")
    verif_matrice = matrice[case[0]][case[1]+1]  # recupertion de la valeur dans la case a droite du personnage
    if verif_matrice in [0, 2, 4]:  # verification de  cette valeur
        tracer_case(case, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        case = case_mouvement
        position_personage = position_centre_carrer(coordonnees(case, pas))
        teleport(position_personage[0], position_personage[1])
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)
        if verif_matrice == 4:
            ramasser_objet(matrice, case, objet_recuperer, dict_objet)
    elif verif_matrice == 3:
        case = poser_question(matrice, case, case_mouvement)
        position_personage = position_centre_carrer(coordonnees(case, pas))  # coordonne du centre du carrer
        teleport(position_personage[0], position_personage[1])  # positionne le turtle au centre du carrer
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)  # redessine le personnage
    onkeypress(deplacer_droite, "Right")


def deplacer_haut():
    """
    deplacer le personnage sur la case au dessus
    """
    global matrice
    global case
    global objet_recuperer
    global dict_objet
    case_mouvement = (case[0]-1, case[1])
    onkeypress(None, "Up")
    verif_matrice = matrice[case[0]-1][case[1]]  # recupertion de la valeur dans la case au dessus du personnage
    if verif_matrice in [0, 2, 4]:  # verification de  cette valeur
        tracer_case(case, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        case = case_mouvement
        position_personage = position_centre_carrer(coordonnees(case, pas))
        teleport(position_personage[0], position_personage[1])
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)
        if verif_matrice == 4:
            ramasser_objet(matrice, case, objet_recuperer, dict_objet)
    elif verif_matrice == 3:
        case = poser_question(matrice, case, case_mouvement)
        position_personage = position_centre_carrer(coordonnees(case, pas))  # coordonne du centre du carrer
        teleport(position_personage[0], position_personage[1])  # positionne le turtle au centre du carrer
        dot((calculer_pas(matrice) * RATIO_PERSONNAGE), COULEUR_PERSONNAGE)  # redessine le personnage
    onkeypress(deplacer_haut, "Up")


def creer_dictionnaire_des_objets(fichier_des_objets):
    """
    lecture du fichier contenant la listes des objet et leur emplacement
    :param fichier_des_objets: fichiers contenant la liste des objets
    :return: retourne la liste des objets dans un dictionnaire
    """
    dict_objet = {}    # initialisation du dictionnaire à retourner
    with open(fichier_des_objets, 'r', encoding='utf-8') as objets:
        liste_objet = objets.read().split('\n')  # stochage de la liste des objets dans une variable
        for objet in liste_objet:
            indice, valeur = eval(objet)  # recuperation de l'indice et de la valeur de l'objet
            dict_objet[indice] = valeur  # ajout de lobjet dans le dictionnaire
    return dict_objet


def trace_rectangle():
    """
    trace un rectangle afin d'effacer une annonce
    :return:
    """
    begin_fill()
    color("white", "white")
    for i in range(2):  # trace un retangle afin de cacher le message precedent
        fd(600)
        for j in range(1):
            left(90)
            fd(25)
            left(90)
    end_fill()


def ramasser_objet(matrice, case, objet_recuperer, dit_objet):
    """
    affichage de l'inventaire et modification d'une
    valeur dans la matrice contenant le plan
    :param matrice: liste conte nant le plan
    :param case: (ligne et colonne ) oou se trouve le turtle
    :param objet_recuperer: liste contenant les objets deja recuperer par le joueur
    :param dit_objet: liste conteant tout les objets a recupere
    """
    global POINT_AFFICHAGE_INVENTAIRE
    matrice[case[0]][case[1]] = 0   # modifi la valeur dans la matrice
    objet_recuperer.append(dit_objet[(case[0], case[1])])  # ajout de l'objet a l'inventaire
    num_objet = len(objet_recuperer)
    teleport(POINT_AFFICHAGE_ANNONCES[0], POINT_AFFICHAGE_ANNONCES[1])  # positionne le turtle au coordonne des anonces
    trace_rectangle()
    color("black")
    teleport(POINT_AFFICHAGE_ANNONCES[0], POINT_AFFICHAGE_ANNONCES[1])
    anonce = "Vous avez trouvé un objet : " + dit_objet[(case[0], case[1])]
    write(anonce, False, font=('Arial', 10, 'normal'))  # ecrit la nouvelle anonce
    color("black")
    message_inventaire = "N°" + str(num_objet) + " " + objet_recuperer[num_objet-1]  # message ajouté dans linventaire
    teleport(POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - 20)   # turtle au coordonne de l'inventaire
    write(message_inventaire, False, font=('Arial', 10, 'normal'))   # affiche le nouveau objet
    POINT_AFFICHAGE_INVENTAIRE = (POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - 20)


def poser_question(matrice, case, mouvement):
    """
    afficher dans le bandeau d’annonces Cette porte est fermée.,
    poser au joueur la question correspondant à l’emplacement de la porte et saisir sa réponse,
    si la réponse est bonne, remplacer la porte par une case vide,
    afficher dans le bandeau d’annonce que la porte s’ouvre, et avancer le personnage,
    si la réponse est mauvaise, l'annoncer et ne pas déplacer le personnage.
    :param matrice: liste contenant le plan
    :param case: coordonne actuel du personnage (ligne , colonne)
    :param mouvement: deplacement souhaité par l'utilisateur (ligne , colonne)
    :return: la position de la (ligne, colonne)
    """
    global dict_porte
    teleport(POINT_AFFICHAGE_ANNONCES[0], POINT_AFFICHAGE_ANNONCES[1])  # positionne le turtle au coordonne des anonces
    trace_rectangle()   # trace un rectangle et le rempli en blanc pour effacer l'annonce precedente
    color("black")  # redonne la couleur noir a le turtle
    write("porte fermer", False, font=('Arial', 10, 'normal'))  # ecrit la nouvelle anonce
    question = dict_porte[mouvement[0], mouvement[1]][0]   # recupere l'enigme dans le turple stocker dans dictionnaire
    reponse = dict_porte[mouvement[0], mouvement[1]][1]  # recupere la reponse dans le turple stocker dans dictionnaire
    reponse_joueur = textinput("Enigme", question)  # afiiche la question au joueur et recupere ca reponse
    listen()
    teleport(POINT_AFFICHAGE_ANNONCES[0], POINT_AFFICHAGE_ANNONCES[1])
    trace_rectangle()
    color("black")
    if reponse_joueur == reponse:   # verifie si la reponse du joueur est correct
        teleport(POINT_AFFICHAGE_ANNONCES[0], POINT_AFFICHAGE_ANNONCES[1])
        write("porte ouverte !", False, font=('Arial', 10, 'normal'))  # ecrit la nouvelle anonce
        tracer_case(case, (COULEURS[0], COULEURS[5]), pas)  # retrace le carrer et efface le personnage
        case = mouvement
        matrice[case[0]][case[1]] = 0
    else:
        teleport(POINT_AFFICHAGE_ANNONCES[0], POINT_AFFICHAGE_ANNONCES[1])
        write("reponse fausse porte fermer !", False, font=('Arial', 10, 'normal'))  # ecrit la nouvelle anonce
        case = case
    return case


ht()  # rendre la turtle invisible
speed(0)
matrice = lire_matrice(fichier_plan)  # recuperation de la matrice
teleport(POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1])  # posionne turtle  au coordonné de l'inventaire
write("Inventaire :", False, font=('Arial', 12, 'normal'))  # ecrit "Inventaite"
teleport(POINT_AFFICHAGE_ANNONCES[0], POINT_AFFICHAGE_ANNONCES[1])  # posionne turtle  au coordonné des anonces
write("Anonce :", False, font=('Arial', 10, 'normal'))
objet_recuperer = []  # initialisation de lensemble contenant l'inventaire objets ramassés
dict_objet = creer_dictionnaire_des_objets("dico_objets.txt")  # dictionnaire contenant la listes des objets à recuperer
dict_porte = creer_dictionnaire_des_objets("dico_portes.txt")
afficher_plan(matrice)  # appel de la fonction pour affichage du plan
pas = calculer_pas(matrice)  # recuperation du pas (dimenssion)
case = POSITION_DEPART  # cases de depart du personnage
depart_pixel_turtle = position_centre_carrer(coordonnees(case, pas))   # de depart en pixel turtle du joueur
teleport(depart_pixel_turtle[0], depart_pixel_turtle[1])
dot((calculer_pas(matrice)*RATIO_PERSONNAGE), COULEUR_PERSONNAGE)
listen()
onkeypress(deplacer_bas, "Down")
onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
onkeypress(deplacer_droite, "Right")
onkeypress(deplacer_haut, "Up")
mainloop()

