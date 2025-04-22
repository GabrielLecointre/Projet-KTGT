import csv

# Lire le fichier CSV avec la librairie csv
with open('donnees_jeux_olympiques/athlete_events.csv', 'r', encoding='utf-8') as donnees:
    lecteur = csv.reader(donnees)
    tableau = list(lecteur)  # Convertir en liste de listes

# Déterminez le nombre de médailles gagnées par Michael Phelps. Son nom complet est
# Michael Fred Phelps, II.
nb_rows = len(tableau)
n_cols = len(tableau[0])

no_medaille = 0  #compteur d'épreuves non médaillées
medaille = 0   #compteur d'épreuves médaillées
compt = 0   #compteur de nombre de participations à une épreuve
for i in range(nb_rows):
    # colonne 2 = rang 1 en python (Nom du participant)
    if "michael fred phelps" in tableau[i][1].lower():
        # lorsque la ligne i concerne michael fred phelps
        # chaque ligne i concerne un particpant et une épreuve
        compt += 1
        print(tableau[i][1], tableau[i][14])
        nom = tableau[i][1]
        #le champ médaille est renseigné à NA si aucune médaille
        if tableau[i][14] == "NA":
            no_medaille += 1
        #colonne
        elif ("Gold" or "Silver" or "Bronze" in tableau[i][15]):
            medaille += 1
print(nom,
      "\nNombre d'épreuves non médaillées : ", no_medaille,
      "\nNombre de médailles : ", medaille,
      "\nNombre de participations aux épreuves : ", compt)
