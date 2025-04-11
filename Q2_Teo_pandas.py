# Jeux de Los Angeles 1984 :
# Quelle a été la performance détaillée de la Roumanie lors des JO de 1984,
# où elle a terminé deuxième au classement des médailles avec 20 médailles d'or,
# 16 d'argent et 17 de bronze ?

import pandas as pd

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv")
pays = pd.read_csv("noc_regions.csv")

# afficher quelques informations sur la base
# print(donnees.head(5))
print(donnees.columns.tolist())
# print(donnees.info())
# print(donnees.describe())
print(pays.columns.tolist())

# jointure pour récupérer le libellé pays pour les NOC
donnees_jo = pd.merge(
    donnees,
    pays[["NOC", "region"]],
    on="NOC",
    how="left",
)
print(donnees_jo.columns.tolist())


def correct_collective_medals(df):
    collective_events = df.groupby(["Games", "Event", "Team"])["ID"].nunique()
    collective_events = (
        collective_events[collective_events > 1]
        .index.get_level_values("Event")
        .unique()
    )

    df_collective = df[df["Event"].isin(collective_events)].copy()
    df_individual = df[~df["Event"].isin(collective_events)].copy()

    def process_collective(group):
        if len(group) >= 6:
            return group.drop_duplicates(
                subset=["region", "Event", "Medal"], keep="first"
            )
        else:
            return group

    corrected_collective = (
        df_collective.groupby(["Games", "Event"])
        .apply(process_collective)
        .reset_index(drop=True)
    )

    return pd.concat([corrected_collective, df_individual], ignore_index=True)


# Assuming your DataFrame is named 'olympics_data'
olympics_corrected = correct_collective_medals(donnees_jo.copy())


def classement_jo(donnees, annee, nb_pays=15):
    """
    Affiche le classement des pays aux JO selon les médzailles obtenues

    Paramètres:
    - donnees: la table des JO
    - annee: l'année des JO qu l'on souhaite afficher
    - nb_pays: Nombre de pays à lister dans le classement (par défaut: 15)

    Retourne:
    - DataFrame contenant le classement des pays
    """
    # permet de filtrer les données pour garder uniquement l'année spécifiée
    jo_annee = donnees[donnees["Year"] == annee]
    jo_medailles = jo_annee[jo_annee["Medal"].notnull()]

    # Créer une table pivot pour compter les médailles par type
    medailles_par_pays = pd.pivot_table(
        jo_medailles,
        index="region",
        columns="Medal",
        aggfunc="size",
        fill_value=0,
    )

    # S'assurer que toutes les colonnes de médailles existent
    for medal in ["Gold", "Silver", "Bronze"]:
        if medal not in medailles_par_pays.columns:
            medailles_par_pays[medal] = 0

    # ordre d'affichage souhaité
    medal_order = ["Gold", "Silver", "Bronze"]

    # imposer l'ordre souhaité
    medailles_par_pays = medailles_par_pays[medal_order]

    # Calculer le total des médailles
    medailles_par_pays["Total"] = medailles_par_pays.sum(axis=1)

    # Trier UNIQUEMENT par médailles d'or
    classement = medailles_par_pays.sort_values(by="Gold", ascending=False)

    return classement.head(nb_pays)


# Exemple d'utilisation
classement_1984 = classement_jo(donnees_jo, 1984)
print("Classement des pays aux JO de 1984 :")
print(f"{classement_1984}")
