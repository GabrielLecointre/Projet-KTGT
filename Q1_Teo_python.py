import os
import csv

# Lire le fichier CSV manuellement et stocker les lignes dans une liste

tableau = []
with open(os.path.join("athlete_events.csv")) as donnees:
    file = csv.reader(donnees)
    for line in file:
        tableau.append(line)

print(len(tableau))
print(tableau[0])
noms_colonnes = tableau[0]  # La première ligne contient les noms des colonnes
for indice, nom_colonne in enumerate(noms_colonnes):
    print(f"Indice {indice}: {nom_colonne}")

# Only five athletes have won medals in both the Winter and the Summer Olympics.
# Only one of them, Christa Ludinger-Rothenburger, won medals in the same year.

# Suppression des lignes où "Medal" est None (si jamais), et des cas ='NA'
donnees_filtrees = [
    ligne for ligne in tableau if ligne[-1] is not None and ligne[-1] != "NA"
]  # car Medal est le dernier indice


def trouver_athletes_ete_hiver(base):
    # Créer un dictionnaire pour stocker les informations par ID d'athlète
    athletes_par_id = {}

    # Parcourir les données pour les regrouper par ID
    for ligne in base:  # pour chaque ligne
        id = ligne[0]  # on récupère le ID, position 0
        if id not in athletes_par_id:  # si l'ID n'existe pas
            athletes_par_id[id] = []  # on le crée
        athletes_par_id[id].append(ligne)  # et on ajoute la ligne correspondante

    athletes_ete_hiver = []

    # Traiter chaque athlète
    for id, participations in athletes_par_id.items():
        # Extraire les saisons uniques pour cet athlète
        saisons = set()
        for p in participations:
            saisons.add(p[10])
        saisons = list(saisons)

        # Collecter les sports par saison
        sports_par_saison = {}
        for p in participations:
            saison = p[10]
            if saison not in sports_par_saison:
                sports_par_saison[saison] = set()
            sports_par_saison[saison].add(p[12])

        # Vérifier si l'athlète a participé à plus d'une saison dans des sports
        # différents
        sports_hiver = set(sports_par_saison.get("Winter", []))
        sports_ete = set(sports_par_saison.get("Summer", []))

        if len(saisons) > 1 and len(sports_hiver & sports_ete) == 0:
            # Collecter les médailles et années par saison
            medaille_annee = {}
            annees_saison = {}

            for saison in saisons:
                medaille_annee[saison] = []
                annees_saison[saison] = []

                for p in participations:
                    if p[10] == saison:
                        if "Medal" in p and p[10]:
                            medaille_annee[saison].append(p[-1])
                        annees_saison[saison].append(p[9])

            # Trouver les années communes entre été et hiver
            annees_ete = set(annees_saison.get("Summer", []))
            annees_hiver = set(annees_saison.get("Winter", []))
            deux_saisons = annees_hiver & annees_ete

            # Ajouter l'athlète à la liste
            athletes_ete_hiver.append(
                {
                    "ID": id,
                    "Name": participations[0][1],
                    "Seasons": saisons,
                    "medaille_annee": medaille_annee,
                    "annees_saison": annees_saison,
                    "deux_saisons": list(deux_saisons),
                }
            )

    return athletes_ete_hiver


# Trouver les athlètes avec des médailles dans différentes saisons
athletes_ete_hiver = trouver_athletes_ete_hiver(donnees_filtrees)

# Afficher les résultats
print("Athlètes ayant remporté des médailles dans différentes saisons :")
for athlete in athletes_ete_hiver:
    # Préparer la liste des années par saison
    years_list = [
        athlete["annees_saison"].get(saison, []) for saison in ["Summer", "Winter"]
    ]

    print(f"ID: {athlete['ID']}")
    print(f"Nom: {athlete['Name']}")
    print(f"Saisons: {athlete['Seasons']}")
    print(f"Années: {years_list}")
    print()

# Afficher les résultats
print("Athlètes ayant remporté des médailles dans différentes saisons la même année :")
for athlete in athletes_ete_hiver:
    # Préparer la liste des années par saison
    years_list = [
        athlete["annees_saison"].get(saison, []) for saison in ["Summer", "Winter"]
    ]
    if athlete["deux_saisons"]:
        print(f"ID: {athlete['ID']}")
        print(f"Nom: {athlete['Name']}")
        print(f"Années: {years_list}")
        print(f"Années communes: {sorted(athlete['deux_saisons'])}")
        print()

# Export simple sans Pandas
nom_fichier_export = "athletes_multi_saisons.csv"
with open(nom_fichier_export, "w", newline="") as fichier_csv:
    writer = csv.writer(fichier_csv)
    # Écrire l'en-tête
    writer.writerow(
        [
            "ID",
            "Nom",
            "Saisons",
            "Médailles Été",
            "Médailles Hiver",
            "Années Été",
            "Années Hiver",
            "Années Communes",
        ]
    )
    # Écrire les données des athlètes
    for athlete in athletes_ete_hiver:
        writer.writerow(
            [
                athlete["ID"],
                athlete["Name"],
                ", ".join(athlete["Seasons"]),
                ", ".join(athlete["medaille_annee"].get("Summer", [])),
                ", ".join(athlete["medaille_annee"].get("Winter", [])),
                ", ".join(map(str, athlete["annees_saison"].get("Summer", []))),
                ", ".join(map(str, athlete["annees_saison"].get("Winter", []))),
                ", ".join(map(str, athlete["deux_saisons"])),
            ]
        )
