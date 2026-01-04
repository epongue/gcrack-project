import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pandas as pd


def translation_rotation(points, a, b, alpha_deg, s):
    """
    Applique d'abord une translation de vecteur (a, b), puis une rotation d'angle alpha (en degrés) autour de l'origine à un ou plusieurs points du plan.
    Paramètres :
        points : tuple (x, y) ou liste de tuples [(x1, y1), (x2, y2), ...]
        a, b   : composantes de la translation
        alpha_deg : angle de rotation (en degrés)
        s       : échelle de passage du pixel au mètre
    Retour :
        Liste de tuples représentant les points transformés.
    """
    # Conversion de l'angle en radians
    alpha = np.radians(alpha_deg)

    # Matrice de rotation
    R = np.array([[np.cos(alpha), -np.sin(alpha)],
                  [np.sin(alpha),  np.cos(alpha)]])

    # Mise en forme de l'entrée
    if isinstance(points, tuple):
        points = [points]

    # Appliquer la translation puis la rotation
    points_transformes = []
    for x, y in points:
        translation = np.array([x - a, y - b])      # Translation
        rotation = R @ translation                   # Rotation  
        pt_reels_rotes = s * rotation
        points_transformes.append(tuple(pt_reels_rotes))  # Stocker le résultat

    return points_transformes 

def symetrie_centrale(points):
    """Cette fonction nous permet d'avoir l'autre moitié de la trajectoire de fissure après la simulation"""
    # Conversion de l'angle en radians
    alpha = np.radians(180)  # Angle de rotation en degrés

    # Matrice de rotation
    R = np.array([[np.cos(alpha), -np.sin(alpha)],
                  [np.sin(alpha),  np.cos(alpha)]])

    # Mise en forme de l'entrée
    if isinstance(points, tuple):
        points = [points]

    # Appliquer la translation puis la rotation
    points_transformes = []
    for x, y in points:      
        rotation = R @ np.array([x, y])                   # Rotation  
        points_transformes.append(tuple(rotation))  # Stocker le résultat

    return points_transformes



def transformation2(points, a, b, alpha_deg, s):
    """
    Applique d'abord une translation de vecteur (a, b), puis une symétrie d'axe (oy), puis une rotation d'angle alpha (en degrés)
    autour de l'origine à un ou plusieurs points du plan.
    Paramètres :
        points : tuple (x, y) ou liste de tuples [(x1, y1), (x2, y2), ...]
        a, b   : composantes de la translation
        alpha_deg : angle de rotation (en degrés)
        s       : échelle de passage du pixel au mètre
    Retour :
        Liste de tuples représentant les points transformés.
    """
    # Conversion de l'angle en radians
    alpha = np.radians(alpha_deg)

    # Matrice de rotation
    R = np.array([[np.cos(alpha), -np.sin(alpha)],
                  [np.sin(alpha),  np.cos(alpha)]])
    
    S = np.array([[-1, 0],
                  [0, 1]])

    # Mise en forme de l'entrée
    if isinstance(points, tuple):
        points = [points]

    # Appliquer la translation puis la rotation
    points_transformes = []
    for x, y in points:
        translation = np.array([x - a, y - b])      # Translation
        symetrie = S @ translation                   # Symétrie
        rotation = R @ symetrie                   # Rotation  
        pt_reels_rotes = s * rotation
        points_transformes.append(tuple(pt_reels_rotes))  # Stocker le résultat

    return points_transformes





def affichage(points_som_rec, pts_funambuleH, pts_funambuleB, point_simH1, point_simB1, point_simH2, point_simB2, 
point_simH6, point_simB6, point_simH7, point_simB7, titre ="title"):
    """
    Affiche les points d'origine et les points transformés côte à côte dans deux sous-figures.
    Paramètres :
        points_transformes : liste de tuples [(x1', y1'), ...] en mètres ou après transformation
        points_som_rec : liste de 4 sommets [(x_A1, y_A1), (x_A2, y_A2), (x_A4, y_A4), (x_A3, y_A3)]
        donnés dans l'ordre A1→A2→A4→A3
    """

    # Séparation des coordonnées
    x_som_rec, y_som_rec = zip(*points_som_rec)
    x_funambuleH, y_funambuleH = zip(*pts_funambuleH)
    x_funambuleB, y_funambuleB = zip(*pts_funambuleB)
    x_simH1, y_simH1 = zip(*point_simH1)
    x_simB1, y_simB1 = zip(*point_simB1)
    x_simH2, y_simH2 = zip(*point_simH2)
    x_simB2, y_simB2 = zip(*point_simB2)
    x_simH6, y_simH6 = zip(*point_simH6)
    x_simB6, y_simB6 = zip(*point_simB6)
    x_simH7, y_simH7 = zip(*point_simH7)
    x_simB7, y_simB7 = zip(*point_simB7)

    # Pour tracer le contour, on boucle à A1
    x_rect = list(x_som_rec) + [x_som_rec[0]]
    y_rect = list(y_som_rec) + [y_som_rec[0]]

    # Création de deux sous-figures côte à côte
    fig, ax = plt.subplots(figsize=(7, 7))



    # Tracé des différents ensembles de points sur le premier subplot
    # ax.scatter(x_funambuleH, y_funambuleH, color='blue', marker='x', label='Funambule H')
    plt.plot(x_funambuleH, y_funambuleH, color='blue', marker=None, label='fissure expérimentale')
    # ax.scatter(x_funambuleB, y_funambuleB, color='magenta', marker='x', label='Funambule B')
    plt.plot(x_funambuleB, y_funambuleB, color='blue', marker=None, label=None)
    # ax.scatter(a, b, color='red', marker='o', label='centre')
    # ax.plot(x_rect, y_rect, color='grey', linestyle='-', linewidth=1.5, label='Bordure de l\'éprouvette')
    ax.plot(x_simH1, y_simH1, color='red', linestyle=':', label='fissure numérique s = 0', linewidth=2)
    ax.plot(x_simB1, y_simB1, color='red', linestyle=':',  label=None, linewidth=2)
    ax.plot(x_simH2, y_simH2, color='olive', linestyle='--', label='fissure numérique s = 0.5da')
    ax.plot(x_simB2, y_simB2, color='olive', linestyle='--', label=None)
    ax.plot(x_simH6, y_simH6, color='purple', linestyle='-.', label='fissure numérique s = 10da')
    ax.plot(x_simB6, y_simB6, color='purple', linestyle='-.', label=None)
    # ax.plot(x_simH7, y_simH7, color='olive', linestyle='-.', label='s = 20da')
    # ax.plot(x_simB7, y_simB7, color='olive', linestyle='-.', label=None)
    
    

    # Personnalisation du graphe
    ax.set_title(titre, fontsize=20)
    ax.set_xlabel("X en mètres", fontsize=20)
    ax.set_ylabel("Y en mètres", fontsize=20)
    ax.axis('equal')
    ax.grid(True)
    ax.legend(fontsize=20)
    ax.set_xlim(-0.015, 0.015)  # Ajuster les limites X
    ax.set_ylim(-0.005, 0.005)  # Ajuster les limites Y

    # Affichage global
    plt.tight_layout()
    plt.show()


##--------------Debut-------------------------------------------------------------------------------------------

angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

# Lire le fichier Excel des données expérimentales
df = pd.read_excel("Dimensions_eprouvettes.xlsx", sheet_name=0)  

# Extraire la colonne des échelles s
scale = df["scale for converting virtual dimensions to real dimensions"]

# Convertir en liste 
scale_list = scale.tolist()

folder1 = 'specimen_data'
folder = 'influence_T-stress'


for i in range(len(angle)):

    # extraction des sommets et du centre de l'éprouvette, notons que le rectangle est nommé A1A2A4A3 dans le sens direct
    x_A1 = df.iloc[i, 7]
    y_A1 = df.iloc[i, 8]

    x_A2 = df.iloc[i, 9]
    y_A2 = df.iloc[i, 10]

    x_A3 = df.iloc[i, 11]
    y_A3 = df.iloc[i, 12]

    x_A4 = df.iloc[i, 13]
    y_A4 = df.iloc[i, 14]

    x_sommet = [x_A1, x_A2, x_A4, x_A3]  # Liste des coordonnées X des sommets
    y_sommet = [y_A1, y_A2, y_A4, y_A3]  # Liste des coordonnées Y des sommets

    # Convertir les coordonnées des sommets en liste de tuples
    sommet = list(zip(x_sommet, y_sommet))  # Liste de tuples des sommets

    # Centre des éprouvettes
    x_centre = df.iloc[i, 15]
    y_centre = df.iloc[i, 16]
    centre = (x_centre, y_centre)


    
    if i==9 or i== 14 :
        # Read the mat file
        fichier = angle[i]
        data_rawH = scipy.io.loadmat(f'{folder1}/angle_'+str(fichier)+'_test_1/funambule_H.mat')
        data_rawB = scipy.io.loadmat(f'{folder1}/angle_'+str(fichier)+'_test_1/funambule_B.mat')

        # Get the data H
        x_rawH = data_rawH["xp"][0]
        y_rawH = data_rawH["yp"][0]

        # Get the data B
        x_rawB = data_rawB["xp"][0]
        y_rawB = data_rawB["yp"][0]

        # Inversion de l'axe Y pour se mettre dans le référentiel de l'image
        y_rawH = -y_rawH  
        y_rawB = -y_rawB

        # Convertir les données en liste de tuples
        points_rawH = list(zip(x_rawH, y_rawH))  # [(x0, y0), (x1, y1), ...]
        points_rawB = list(zip(x_rawB, y_rawB))  # [(x0, y0), (x1, y1), ...]

        #lecture des données de la simulation
        df1 = pd.read_csv(f'{folder}/Resultats_s=0/results_'+str(angle[i])+'.csv')
        df2 = pd.read_csv(f'{folder}/Resultats_s=0.5da/results_'+str(angle[i])+'.csv')
        df6 = pd.read_csv(f'{folder}/Resultats_s=10da/results_'+str(angle[i])+'.csv')
        df7 = pd.read_csv(f'{folder}/Resultats_s=20da/results_'+str(angle[i])+'.csv')

        # Obtention des points du chemin de la fissure après la simulation
        x_sim1 = df1["xc_1"].tolist()  
        y_sim1 = df1["xc_2"].tolist()
        point_simH1 = list(zip(x_sim1, y_sim1))

        x_sim2 = df2["xc_1"].tolist()
        y_sim2 = df2["xc_2"].tolist()
        point_simH2 = list(zip(x_sim2, y_sim2))

        x_sim6 = df6["xc_1"].tolist()
        y_sim6 = df6["xc_2"].tolist()
        point_simH6 = list(zip(x_sim6, y_sim6))

        x_sim7 = df7["xc_1"].tolist()
        y_sim7 = df7["xc_2"].tolist()
        point_simH7 = list(zip(x_sim7, y_sim7))

        # symétrie d'axe (oy) des points du chemin de la fissure
        point_simB1 = symetrie_centrale(points =point_simH1)
        point_simB2 = symetrie_centrale(points =point_simH2)
        point_simB6 = symetrie_centrale(points =point_simH6)
        point_simB7 = symetrie_centrale(points =point_simH7)

        #transformation des sommmets
        points_transform_sommet = transformation2(
            points=sommet,
            a= x_centre,
            b= y_centre,
            alpha_deg=-90,
            s= scale_list[i]  # Utilisation de l'échelle correspondante
        )

        # Transformation des pointsH
        points_transformH = transformation2(
            points=points_rawH,
            a= x_centre,
            b= y_centre,
            alpha_deg=-90,
            s= scale_list[i]  # Utilisation de l'échelle correspondante
        )
        # transformation des pointsB
        points_transformB = transformation2(
            points=points_rawB,
            a= x_centre,
            b= y_centre,
            alpha_deg=-90,
            s= scale_list[i]  # Utilisation de l'échelle correspondante
        )

        # Affichage des points transformés
        affichage(
            points_som_rec=points_transform_sommet,
            pts_funambuleH=points_transformH,
            pts_funambuleB=points_transformB,
            point_simH1=point_simH1,
            point_simB1=point_simB1,
            point_simH2=point_simH2,
            point_simB2=point_simB2,
            point_simH6=point_simH6,
            point_simB6=point_simB6,
            point_simH7=point_simH7,
            point_simB7=point_simB7,
            titre=f"Angle {angle[i]}°"
        )

    elif i==1 or i==3 :
        # Read the mat file
        fichier = angle[i]
        data_rawH = scipy.io.loadmat(f'{folder1}/angle_'+str(fichier)+'_test_1/funambule_H.mat')
        data_rawB = scipy.io.loadmat(f'{folder1}/angle_'+str(fichier)+'_test_1/funambule_B.mat')

        # Obtention des données funambule H
        x_rawH = data_rawH["xp"][0]
        y_rawH = data_rawH["yp"][0]

        # Obtention des données funambule B
        x_rawB = data_rawB["xp"][0]
        y_rawB = data_rawB["yp"][0]

        # Inversion de l'axe Y pour se mettre dans le référentiel de l'image
        y_rawH = -y_rawH  
        y_rawB = -y_rawB

        # Convertir les données en liste de tuples
        points_rawH = list(zip(x_rawH, y_rawH))  # [(x0, y0), (x1, y1), ...]
        points_rawB = list(zip(x_rawB, y_rawB))  # [(x0, y0), (x1, y1), ...]

        #lecture des données de la simulation
        df1 = pd.read_csv(f'{folder}/Resultats_s=0/results_'+str(angle[i])+'.csv')
        df2 = pd.read_csv(f'{folder}/Resultats_s=0.5da/results_'+str(angle[i])+'.csv')
        df6 = pd.read_csv(f'{folder}/Resultats_s=10da/results_'+str(angle[i])+'.csv')
        df7 = pd.read_csv(f'{folder}/Resultats_s=20da/results_'+str(angle[i])+'.csv')

        # Obtention des points du chemin de la fissure après la simulation
        x_sim1 = df1["xc_1"].tolist()  
        y_sim1 = df1["xc_2"].tolist()
        point_simH1 = list(zip(x_sim1, y_sim1))

        x_sim2 = df2["xc_1"].tolist()
        y_sim2 = df2["xc_2"].tolist()
        point_simH2 = list(zip(x_sim2, y_sim2))

        x_sim6 = df6["xc_1"].tolist()
        y_sim6 = df6["xc_2"].tolist()
        point_simH6 = list(zip(x_sim6, y_sim6))

        x_sim7 = df7["xc_1"].tolist()
        y_sim7 = df7["xc_2"].tolist()
        point_simH7 = list(zip(x_sim7, y_sim7))

        # symétrie centrale des points du chemin de la fissure
        point_simB1 = symetrie_centrale(points =point_simH1)
        point_simB2 = symetrie_centrale(points =point_simH2)
        point_simB6 = symetrie_centrale(points =point_simH6)
        point_simB7 = symetrie_centrale(points =point_simH7)
        
        # Convertir les points du chemin de la fissure en liste de tuples
        point_simB1 = symetrie_centrale(points = point_simH1)
        point_simB2 = symetrie_centrale(points = point_simH2)
        point_simB6 = symetrie_centrale(points = point_simH6)
        point_simB7 = symetrie_centrale(points = point_simH7)

        #transformation des sommmets
        points_transform_sommet = translation_rotation(
            points=sommet,
            a= x_centre,
            b= y_centre,
            alpha_deg= -90,
            s= scale_list[i]  # Utilisation de l'échelle correspondante
        )

        # Transformation des pointsH
        points_transformH = translation_rotation(
            points=points_rawH,
            a= x_centre,
            b= y_centre,
            alpha_deg= -90,
            s= scale_list[i]  # Utilisation de l'échelle correspondante
        )

        # transformation des pointsB
        points_transformB = translation_rotation(
            points=points_rawB,
            a= x_centre,
            b= y_centre,
            alpha_deg= -90,
            s= scale_list[i]  # Utilisation de l'échelle correspondante
        )

        # Affichage des points transformés
        affichage(
            points_som_rec=points_transform_sommet,
            pts_funambuleH=points_transformH,
            pts_funambuleB=points_transformB,
            point_simH1=point_simH1,
            point_simB1=point_simB1,
            point_simH2=point_simH2,
            point_simB2=point_simB2,
            point_simH6=point_simH6,
            point_simB6=point_simB6,
            point_simH7=point_simH7,
            point_simB7=point_simB7,
            titre=f"Angle {angle[i]}°"
        )
    else:
        print(f"Pas encore de données pour l'angle {angle[i]}°")
        continue
