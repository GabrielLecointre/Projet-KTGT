# Only five athletes have won medals in both the Winter and the Summer Olympics.
# Only one of them, Christa Ludinger-Rothenburger, won medals in the same year.

import pandas as pd

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv")

# Filtrer les données pour garder uniquement les athletes avec médailles
donnees = donnees.dropna(subset=["Medal"])  # supprimer les valeurs manquantes
donnees = donnees[donnees["Medal"] != "NA"]  # Exclure les entrées "NA"


# Trouver les athlètes ayant participé aux Jeux d'été et d'hiver
def trouver_athletes_ete_hiver(df):
    athletes_par_id = df.groupby("ID")

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
            athletes_ete_hiver.append(
                {
                    "ID": id,
                    "Name": group["Name"].iloc[0],
                    "Seasons": list(saison),
                    "Medals": group["Medal"].tolist(),
                    # converts a NumPy array to a Python list without changing its data
                    "Years": group["Year"].tolist(),
                }
            )

    return athletes_ete_hiver


# Trouver les 5 athlètes avec des médailles dans différentes saisons
athletes_ete_hiver = trouver_athletes_ete_hiver(donnees)

# Afficher les résultats
print("Athlètes ayant remporté des médailles dans différentes saisons :")
for athlete in athletes_ete_hiver:
    print(f"\nid: {athlete['ID']}")
    print(f"Nom: {athlete['Name']}")
    print(f"Saisons: {athlete['Seasons']}")
    print(f"Médailles: {athlete['Medals']}")
    print(f"Années: {athlete['Years']}")

# Afficher les 5 premiers résultats
print(athletes_ete_hiver)


# Vérifier s'il y a des athlètes avec des médailles la même année
def trouver_athletes_meme_annee(df):
    # Identifier les athlètes ayant des médailles aux Jeux d'été et d'hiver
    athletes_par_id = df.groupby("ID")
    athletes_medaille_ete_hiver_meme_annee = []

    for id, group in athletes_par_id:
        # Filtrer les médailles uniquement
        group_medailles = group[group["Medal"] != "NA"]

        # Grouper par année
        annees_par_saison = group_medailles.groupby("Year")["Season"].unique()

        # Rechercher les années avec des médailles d'été et d'hiver
        for annee, saisons in annees_par_saison.items():
            if set(saisons) == {"Summer", "Winter"}:
                # Récupérer les détails des médailles pour cette année
                medailles_annee = group_medailles[group_medailles["Year"] == annee]

                athletes_medaille_ete_hiver_meme_annee.append(
                    {
                        "ID": id,
                        "Name": group["Name"].iloc[0],
                        "Year": annee,
                        "Summer_Medals": medailles_annee[
                            medailles_annee["Season"] == "Summer"
                        ]["Medal"].tolist(),
                        "Winter_Medals": medailles_annee[
                            medailles_annee["Season"] == "Winter"
                        ]["Medal"].tolist(),
                        "Summer_Sport": medailles_annee[
                            medailles_annee["Season"] == "Summer"
                        ]["Sport"]
                        .unique()
                        .tolist(),
                        "Winter_Sport": medailles_annee[
                            medailles_annee["Season"] == "Winter"
                        ]["Sport"]
                        .unique()
                        .tolist(),
                    }
                )

    return athletes_medaille_ete_hiver_meme_annee


# Utilisation de la fonction
athletes_meme_annee_ete_hiver = trouver_athletes_meme_annee(donnees)

# Afficher les résultats
print(
    "\nAthlètes ayant remporté des médailles aux Jeux d'été et d'hiver la même année :"
)
for athlete in athletes_meme_annee_ete_hiver:
    print(f"\nNom: {athlete['Name']}")
    print(f"Année: {athlete['Year']}")
    print(f"Sports d'été: {athlete['Summer_Sport']}")
    print(f"Médailles d'été: {athlete['Summer_Medals']}")
    print(f"Sports d'hiver: {athlete['Winter_Sport']}")
    print(f"Médailles d'hiver: {athlete['Winter_Medals']}")
