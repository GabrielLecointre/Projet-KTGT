# Only five athletes have won medals in both the Winter and the Summer Olympics.
# Only one of them, Christa Ludinger-Rothenburger, won medals in the same year.

import pandas as pd

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv")

# Filtrer les données pour garder uniquement les athletes avec médailles
donnees = donnees.dropna(subset=["Medal"])  # supprimer les valeurs manquantes
donnees = donnees[donnees["Medal"] != "NA"]  # Exclure les entrées "NA"


# Trouver les athlètes ayant participé aux Jeux d'été et d'hiver
def trouver_athletes_ete_hiver(base):
    athletes_par_id = base.groupby("ID")

    athletes_ete_hiver = []

    for id, group in athletes_par_id:
        saison = group["Season"].unique()  # garder les éléments uniques d'un tableau
        # Avant 1924 (année de création des jeux d'hiver, les disciplines d'hiver sont
        # incluses dans les sports d'été)
        sports = group.groupby("Season")["Sport"].unique()  # Sports uniques par saison
        # il a participé à plus d'une saison, pas la même discipline
        if (
            len(saison) > 1
            and len(set(sports.get("Winter", [])) & set(sports.get("Summer", []))) == 0
        ):
            # Créer un dictionnaire pour stocker les médailles et années par saison
            medaille_annee = {}
            annees_saison = {}

            for saison in saison:
                donnees_saison = group[group["Season"] == saison]
                medaille_annee[saison] = donnees_saison["Medal"].tolist()
                annees_saison[saison] = donnees_saison["Year"].tolist()

            # Trouver les années communes
            deux_saisons = set(annees_saison.get("Summer", [])) & set(
                annees_saison.get("Winter", [])
            )

            athletes_ete_hiver.append(
                {
                    "ID": id,
                    "Name": group["Name"].iloc[0],
                    "Seasons": list(saison),
                    "medaille_annee": medaille_annee,
                    "annees_saison": annees_saison,
                    "deux_saisons": list(deux_saisons),
                }
            )
    return athletes_ete_hiver


# Trouver les athlètes avec des médailles dans différentes saisons
athletes_ete_hiver = trouver_athletes_ete_hiver(donnees)

# Afficher les résultats
print("Athlètes ayant remporté des médailles dans différentes saisons :")
for athlete in athletes_ete_hiver:
    # Préparer la liste des années par saison
    years_list = [
        athlete['annees_saison'].get(saison, []) for saison in ['Summer', 'Winter']
        ]

    print(f"ID: {athlete['ID']}")
    print(f"Nom: {athlete['Name']}")
    print(f"Années: {years_list}")
    print()

# Afficher les résultats
print("Athlètes ayant remporté des médailles dans différentes saisons la même année :")
for athlete in athletes_ete_hiver:
    # Préparer la liste des années par saison
    years_list = [
        athlete['annees_saison'].get(saison, []) for saison in ['Summer', 'Winter']
        ]
    if athlete['deux_saisons']:
        print(f"ID: {athlete['ID']}")
        print(f"Nom: {athlete['Name']}")
        print(f"Années: {years_list}")
        print(f"Années communes: {sorted(athlete['deux_saisons'])}")
        print()

# test
