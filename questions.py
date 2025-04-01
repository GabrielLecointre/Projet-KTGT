# Jeux Olympiques :

ligne = "  Alice, 23, 17.5  \n"
print(ligne.strip())  # "Alice, 23, 17.5"

texte = "Alice,23,17.5"
print(texte.split(","))  # ["Alice", "23", "17.5"]

# Lire le fichier CSV manuellement et stocker les lignes dans une liste
with open(
    "athlete_events.csv", "r", encoding="utf-8"
) as donnees:
    lignes = donnees.readlines()  # Lire toutes les lignes

# Convertir en tableau (liste de listes)
tableau = [ligne.strip().split(",") for ligne in lignes]

print(len(tableau), len(tableau[0]))


# Déterminez le nombre de médailles gagnées par Michael Phelps. Son nom complet est
# Michael Fred Phelps, II.
# Attention lors du split(), le séparateur pris en compte est la virgule
# donc le II a été créé dans une autre colonne
# il pourrait y avoir Michael Fred Phelps, II et Michael Fred Phelps : 2 personnes
# différentes
nb_rows = len(tableau)
n_cols = len(tableau[0])

no_medaille = 0
medaille = 0
compt = 0
for i in range(nb_rows):
    if "michael fred phelps" in tableau[i][1].lower() and "II" in tableau[i][2]:
        compt += 1
        print(tableau[i][1], tableau[i][2])
        if tableau[i][14] is None:
            no_medaille += 1
        elif "Gold" or "Silver" or "Bronze" in tableau[i][15]:
            medaille += 1
print(no_medaille, medaille, compt)

# Trouvez des bornes inférieures et supérieures pour le nombre de médailles
# par nation pour les Jeux Olympiques de 2016.

for i in range(nb_rows):
    if "CHN" in tableau[i][7]:  # Vérifie si le pays est la Chine (colonne 6)
        compt += 1
        if tableau[i][14] is None:  # Si la médaille est None (manquante)
            no_medaille += 1
        elif any(
            medal in tableau[i][14] for medal in ["Gold", "Silver", "Bronze"]
        ):  # Vérifie si la médaille est or, argent ou bronze
            medaille += 1
print(no_medaille, medaille, compt)


# Initialiser un dictionnaire pour stocker les médailles par pays
medailles_par_pays = {}

# Parcourir toutes les lignes du tableau
for i in range(nb_rows):
    pays = tableau[i][7]  # Le pays est dans la colonne 6
    medaille = tableau[i][14]  # La médaille est dans la colonne 15

    # Vérifier si le pays a une médaille
    if medaille is not None and any(
        medal in medaille for medal in ["Gold", "Silver", "Bronze"]
    ):
        # Si le pays est déjà dans le dictionnaire, ajouter 1 médaille
        if pays in medailles_par_pays:
            medailles_par_pays[pays] += 1
        else:
            # Si le pays n'est pas dans le dictionnaire, l'ajouter avec 1 médaille
            medailles_par_pays[pays] = 1

# Trier le dictionnaire par le nombre de médailles en ordre décroissant
medailles_triees = sorted(medailles_par_pays.items(), key=lambda x: x[1], reverse=True)

# Afficher les résultats
for pays, total_medailles in medailles_par_pays.items():
    print(f"{pays}: {total_medailles} médailles")

# Trouver le pays avec le maximum de médailles
pays_max, medailles_max = max(medailles_par_pays.items(), key=lambda x: x[1])
# Trouver le pays avec le minimum de médailles
pays_min, medailles_min = min(medailles_par_pays.items(), key=lambda x: x[1])

# Afficher la borne supérieure
print(f"La borne supérieur est {medailles_max}")

# Afficher la borne inférieure
print(f"La borne inférieur est {medailles_min} ")
