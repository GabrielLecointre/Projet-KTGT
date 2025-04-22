# Ce programme Python donne les pays qui ont été médaillés
# dans le maximum d’éditions différentes des Jeux Olympiques.
# ATTENTION : CHANGER LE CHEMIN DU FICHIER SI BESOIN
import pandas
import os

pandas.set_option("display.max_rows", 150)

# Lire le fichier .csv avec la base de données (CHEMIN DU FICHIER)
BDJO = pandas.read_csv(os.path.join("donnees_jeux_olympiques", "athlete_events.csv"))
pays = pandas.read_csv(os.path.join("donnees_jeux_olympiques", "noc_regions.csv"))

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

# set_index

# Fusionner les trois DataFrames pour avoir un tableau complet
paysmedailles = pandas.merge(pays_total, pays_ete, on="NOC", how="left")
paysmedailles = pandas.merge(paysmedailles, pays_hiver, on="NOC", how="left")
# jointure
paysmedailles = pandas.merge(
    paysmedailles,
    pays[["NOC", "region"]],
    on="NOC",
    how="left",
)

# Le tableau des pays est imparfait soit 4 corrections à la main :
# SGP = Singapore (manquant)
# HKG = Hong Kong à affecter à Hong Kong et non à China (2 délégations différentes)
# WIF = Indes occidentales à affecter à Jamaica et non à Trinidad (plus logique car
# plus peuplée et les médailles sont remportées par des Jamaïquains)
# GDR = Allemagne de l’Est affecté à East Germany (plus logique car période où
# Allemagne de l’Ouest a aussi sa délégation)

corrections = {
    "SGP": "Singapore",
    "HKG": "Hong Kong",
    "WIF": "Jamaica",
    "GDR": "East Germany",
}

paysmedailles["region"] = (
    paysmedailles["NOC"].map(corrections).fillna(paysmedailles["region"])
)

# On remplace les NaN par des zéros.
paysmedailles.fillna(0, inplace=True)

# On transforme les flottants en entiers.
paysmedailles[["Nb_JO", "Nb_JO_H", "Nb_JO_E"]] = paysmedailles[
    ["Nb_JO", "Nb_JO_H", "Nb_JO_E"]
].astype(int)

paysmedailles_tri = paysmedailles.sort_values(by="Nb_JO", ascending=False)

# Afficher le résultat
print(paysmedailles_tri)
print(paysmedailles_tri.columns)

# Les pays suivants (ou leur prolongement historique) ont eu des médailles sous des
# codes différents selon les périodes, le nom de pays renvoyé par le tableau est
# identique et les données peuvent être sommées :
# ANZ = Australasie (soit Australie + Nouvelle-Zélande) affecté à Australia
# BOH et TCH = Bohême et Tchécoslovaquie (soit République tchèque et Slovaquie)
# affecté à Czech Republic
# YUG et SCG = Yougoslavie (soit 7 pays) et Serbie-et-Monténégro (soit Serbie et
# Monténégro) affecté à Serbia
# URS et EUN = Union soviétique (soit 15 pays) et Équipe unifiée (12 pays)
# affecté à Russia
# FRG = Allemagne de l’Ouest affecté à Germany
# WIF = Indes occidentales affecté à Jamaica
