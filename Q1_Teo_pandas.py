# Only five athletes have won medals in both the Winter and the Summer Olympics.
# Only one of them, Christa Ludinger-Rothenburger, won medals in the same year.
import pandas as pd

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv")

# Filtrer les données pour garder uniquement les athletes avec médailles
donnees = donnees[donnees["Medal"].notnull()]  # filtrer les données sauf NaN


# Trouver les athlètes ayant participé aux Jeux d'été et d'hiver
def trouver_athletes_ete_hiver(base, fichier_excel=None):
    athletes_par_id = base.groupby("ID")

    athletes_ete_hiver = []
    data_pour_excel = []

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

            for s in saison:
                donnees_saison = group[group["Season"] == s]
                medaille_annee[s] = donnees_saison["Medal"].tolist()
                annees_saison[s] = donnees_saison["Year"].tolist()

            # Trouver les années communes
            deux_saisons = set(annees_saison.get("Summer", [])) & set(
                annees_saison.get("Winter", [])
            )

            athlete_info = {
                "ID": id,
                "Name": group["Name"].iloc[0],
                "Seasons": list(saison),
                "medaille_annee": medaille_annee,
                "annees_saison": annees_saison,
                "deux_saisons": list(deux_saisons),
            }
            athletes_ete_hiver.append(athlete_info)
            data_pour_excel.append(athlete_info)

    if fichier_excel:
        df_export = pd.DataFrame(data_pour_excel)
        df_export.to_excel(fichier_excel, index=False)

    return athletes_ete_hiver


# Trouver les athlètes avec des médailles dans différentes saisons
athletes_ete_hiver = trouver_athletes_ete_hiver(
    donnees, fichier_excel="athletes_multi_saisons.xlsx"
)

# Afficher les résultats
print("Athlètes ayant remporté des médailles dans différentes saisons :")
for athlete in athletes_ete_hiver:
    # Préparer la liste des années par saison
    years_list = [
        athlete["annees_saison"].get(saison, []) for saison in ["Summer", "Winter"]
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
        athlete["annees_saison"].get(saison, []) for saison in ["Summer", "Winter"]
    ]
    if athlete["deux_saisons"]:
        print(f"ID: {athlete['ID']}")
        print(f"Nom: {athlete['Name']}")
        print(f"Années: {years_list}")
        print(f"Années communes: {sorted(athlete['deux_saisons'])}")
        print()
