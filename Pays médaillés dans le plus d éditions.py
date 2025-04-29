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

# On regroupe les pays suivants (ou leur prolongement historique) qui ont eu
# des médailles sous des codes différents selon les périodes, le nom de pays
# renvoyé par le tableau est identique et les données peuvent être sommées :
# ANZ = Australasie (soit Australie + Nouvelle-Zélande) affecté à Australia
# BOH et TCH = Bohême et Tchécoslovaquie (soit République tchèque et Slovaquie)
# affecté à Czech Republic (entité principale démographique)
# YUG et SCG = Yougoslavie (soit 7 pays) et Serbie-et-Monténégro (soit Serbie et
# Monténégro) affecté à Serbia (entité démographique principale)
# URS et EUN = Union soviétique (soit 15 pays, Jeux de 1988 et avant)
# et Équipe unifiée (12 pays, Jeux de 1992) affecté à Russia (son entité centrale)
# FRG = Allemagne de l’Ouest affecté à Germany
# WIF = Indes occidentales affecté à Jamaica
paysmedailles = (
    paysmedailles.groupby("region")[["Nb_JO", "Nb_JO_E", "Nb_JO_H"]].sum().reset_index()
)
# Je renomme la colonne "region" en "délégation".
paysmedailles.rename(columns={"region": "délégation"}, inplace=True)
# Je supprime la colonne d'index qui était indésirable
# et je fais de la colonne "region" le nouvel index.
paysmedailles = paysmedailles.set_index("délégation")

# Je classe enfin les pays par ordre décroissant des Jeux où ils ont une médaille
# puis à nombre égal par ordre alphabétique.
paysmedailles_tri = paysmedailles.sort_values(
    by=["Nb_JO", "délégation"], ascending=[False, True]
)

# Afficher le résultat
print(paysmedailles_tri)

'''Ce programme affiche :
                             Nb_JO  Nb_JO_E  Nb_JO_H
délégation
France                          50       29       21
USA                             50       28       22
Canada                          49       27       22
Sweden                          49       27       22
Switzerland                     49       28       21
Austria                         48       26       22
Finland                         48       26       22
Norway                          47       25       22
Germany                         45       25       20
Italy                           45       27       18
UK                              44       29       15
Czech Republic                  41       25       16
Netherlands                     41       26       15
Australia                       36       29        7
Russia                          34       18       16
Hungary                         33       27        6
Japan                           33       21       12
Belgium                         31       27        4
Denmark                         29       28        1
Poland                          28       21        7
New Zealand                     23       22        1
South Korea                     23       16        7
Serbia                          22       20        2
Greece                          21       21        0
Mexico                          21       21        0
Spain                           21       19        2
Bulgaria                        20       16        4
Romania                         20       19        1
Argentina                       19       19        0
Brazil                          19       19        0
India                           19       18        1
South Africa                    18       18        0
Turkey                          17       17        0
China                           16        9        7
Iran                            16       16        0
Jamaica                         16       16        0
Cuba                            15       15        0
Ireland                         15       15        0
Portugal                        15       15        0
Estonia                         13       10        3
Belarus                         12        6        6
Ethiopia                        12       12        0
Kenya                           12       12        0
North Korea                     12       10        2
Croatia                         11        7        4
East Germany                    11        5        6
Latvia                          11        8        3
Mongolia                        11       11        0
Slovenia                        11        7        4
Colombia                        10       10        0
Kazakhstan                      10        6        4
Morocco                         10       10        0
Taiwan                          10       10        0
Thailand                        10       10        0
Trinidad                        10       10        0
Ukraine                         10        6        4
Venezuela                       10       10        0
Bahamas                          9        9        0
Egypt                            9        9        0
Nigeria                          9        9        0
Pakistan                         9        9        0
Slovakia                         9        6        3
Indonesia                        8        8        0
Philippines                      8        8        0
Uruguay                          8        8        0
Algeria                          7        7        0
Chile                            7        7        0
Lithuania                        7        7        0
Puerto Rico                      7        7        0
Tunisia                          7        7        0
Uzbekistan                       7        6        1
Azerbaijan                       6        6        0
Georgia                          6        6        0
Israel                           6        6        0
Luxembourg                       6        5        1
Armenia                          5        5        0
Cameroon                         5        5        0
Dominican Republic               5        5        0
Malaysia                         5        5        0
Uganda                           5        5        0
Ghana                            4        4        0
Iceland                          4        4        0
Liechtenstein                    4        0        4
Moldova                          4        4        0
Peru                             4        4        0
Qatar                            4        4        0
Singapore                        4        4        0
Syria                            4        4        0
Costa Rica                       3        3        0
Haiti                            3        3        0
Hong Kong                        3        3        0
Lebanon                          3        3        0
Tajikistan                       3        3        0
Vietnam                          3        3        0
Zimbabwe                         3        3        0
Afghanistan                      2        2        0
Bahrain                          2        2        0
Burundi                          2        2        0
Ecuador                          2        2        0
Grenada                          2        2        0
Individual Olympic Athletes      2        2        0
Ivory Coast                      2        2        0
Kuwait                           2        2        0
Kyrgyzstan                       2        2        0
Mozambique                       2        2        0
Namibia                          2        2        0
Niger                            2        2        0
Panama                           2        2        0
Saudi Arabia                     2        2        0
Sri Lanka                        2        2        0
Suriname                         2        2        0
United Arab Emirates             2        2        0
Zambia                           2        2        0
Barbados                         1        1        0
Bermuda                          1        1        0
Botswana                         1        1        0
Curacao                          1        1        0
Cyprus                           1        1        0
Djibouti                         1        1        0
Eritrea                          1        1        0
Fiji                             1        1        0
Gabon                            1        1        0
Guatemala                        1        1        0
Guyana                           1        1        0
Iraq                             1        1        0
Jordan                           1        1        0
Kosovo                           1        1        0
Macedonia                        1        1        0
Mauritius                        1        1        0
Monaco                           1        1        0
Montenegro                       1        1        0
Nepal                            1        0        1
Paraguay                         1        1        0
Senegal                          1        1        0
Sudan                            1        1        0
Tanzania                         1        1        0
Togo                             1        1        0
Tonga                            1        1        0
Virgin Islands, US               1        1        0'''
