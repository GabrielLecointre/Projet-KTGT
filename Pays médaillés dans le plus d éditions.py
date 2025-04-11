# Ce programme Python donne les pays qui ont été médaillés
# dans le maximum d’éditions différentes des Jeux Olympiques.
# ATTENTION : CHANGER LE CHEMIN DU FICHIER SI BESOIN
import pandas
import os

pandas.set_option("display.max_rows", 150)

# Lire le fichier .csv avec la base de données (CHEMIN DU FICHIER)
BDJO = pandas.read_csv(os.path.join("donnees_jeux_olympiques", "athlete_events.csv"))

# Comment la taille des sportifs varient-ils selon les sports et le sexe ?

BDJOpaysmedailles = BDJO.dropna(subset=["Medal"])
# Je supprime les lignes sans médailles. Ne reste plus qu’or, argent et bronze.
BDJOpaysmedailles.drop(
    columns=[
        "Name",
        "Age",
        "Weight",
        "Team",
        "City",
        "Event",
        "ID",
        "Sex",
        "Height",
        "Year",
        "Sport",
        "Medal",
    ],
    inplace=True,
)
# Il ne reste plus que les trois colonnes NOC, Games, Season.
# paysmedailles = BDJOpaysmedailles.groupby('NOC')['Games'].nunique().reset_index()
BDJOpaysmedailles.drop_duplicates(keep="first", inplace=True)
# On ne garde qu’une seule donnée par pays pour une édition donnée.

pays_total = BDJOpaysmedailles.groupby("NOC").size().reset_index(name="Nb_JO")

# Compter le nombre de lignes pour chaque pays pour la saison Winter
pays_hiver = (
    BDJOpaysmedailles[BDJOpaysmedailles["Season"] == "Winter"]
    .groupby("NOC")
    .size()
    .reset_index(name="Nb_JO_H")
)

# Compter le nombre de lignes pour chaque pays pour la saison Summer
pays_ete = (
    BDJOpaysmedailles[BDJOpaysmedailles["Season"] == "Summer"]
    .groupby("NOC")
    .size()
    .reset_index(name="Nb_JO_E")
)

# fillna
# set_index
# astype(int)

# Fusionner les trois DataFrames pour avoir un tableau complet
paysmedailles = pandas.merge(pays_total, pays_ete, on="NOC", how="left")
paysmedailles = pandas.merge(paysmedailles, pays_hiver, on="NOC", how="left")
paysmedailles_tri = paysmedailles.sort_values(by="Nb_JO", ascending=False)

# Afficher le résultat
print(paysmedailles_tri)
print(paysmedailles_tri.columns)
