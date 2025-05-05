# Ce programme en Python pur donne les pays qui ont été médaillés
# dans le maximum d’éditions différentes des Jeux Olympiques.
# ATTENTION : CHANGER LE CHEMIN DU FICHIER SI BESOIN
import csv
import os
import time

# Lire les fichiers .csv avec la base de données (CHEMIN DU FICHIER)
chemin_base = "donnees_jeux_olympiques"
BDJO = os.path.join(chemin_base, "athlete_events.csv")
pays = os.path.join(chemin_base, "noc_regions.csv")

debutchrono = time.time()

# On regarde la concordance entre codes utilisés par le C.I.O. et noms des pays.
concordance = {}
with open(pays, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        noc = row["NOC"]
        region = row["region"]
        concordance[noc] = region

# On fait des corrections manuelles sur 4 pays.
corrections = {
    "SGP": "Singapore",
    "HKG": "Hong Kong",
    "WIF": "Jamaica",
    "GDR": "East Germany",
}
concordance.update(corrections)

# On crée un dictionnaire vide pour stocker les éditions avec médailles par pays.
noc_tot = {}  # clé : NOC, valeur : set vide de Jeux été et hiver confondus
noc_e = {}    # clé : NOC, valeur : set vide de Jeux d’été
noc_h = {}    # clé : NOC, valeur : set vide de Jeux d’hiver

# Pour connaître le nombre total d’éditions (été/hiver).
tot_JO = set()
e_JO = set()
h_JO = set()

with open(BDJO, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["Medal"] not in {"Gold", "Silver", "Bronze"}:
            continue  # On ignore les lignes sans médaille

        noc = row["NOC"]
        jeux = row["Games"]
        saison = row["Season"]

        tot_JO.add(jeux)
        if saison == "Summer":  # Jeux d’été
            e_JO.add(jeux)
        else:  # Forcément "Winter" pour ceux d’hiver.
            h_JO.add(jeux)

        # Initialisation des sets si nécessaires
        if noc not in noc_tot:
            noc_tot[noc] = set()
            noc_e[noc] = set()
            noc_h[noc] = set()

        noc_tot[noc].add(jeux)
        if saison == "Summer":
            noc_e[noc].add(jeux)
        else:
            noc_h[noc].add(jeux)

# On fusionne les délégations qui ont eu une continuité historique :
# Union soviétique -> équipe unifiée (1992) -> Russie
# Bohême -> Tchécoslovaquie -> Tchéquie
# Jamaïque -> Indes occidentales -> Jamaïque
# Allemagne -> Allemagne de l’Ouest -> Allemagne
# Yougoslavie -> Serbie-et-Monténégro -> Serbie
table_pays = {}
regroupements = {}

for noc in noc_tot:
    pays = regroupements.get(noc, concordance.get(noc, noc))
    if pays not in table_pays:
        table_pays[pays] = {
            "total": set(),
            "ete": set(),
            "hiver": set()
        }

    table_pays[pays]["total"].update(noc_tot[noc])
    table_pays[pays]["ete"].update(noc_e[noc])
    table_pays[pays]["hiver"].update(noc_h[noc])

# On crée le tableau final.
# Calcul ligne "TOTAL"
total_ligne = {
    "délégation": "TOTAL",
    "Nb_JO": len(tot_JO),
    "Nb_JO_E": len(e_JO),
    "Nb_JO_H": len(h_JO),
}

# Liste des résultats par pays
resultats = []

for pays, data in table_pays.items():
    resultats.append({
        "délégation": pays,
        "Nb_JO": len(data["total"]),
        "Nb_JO_E": len(data["ete"]),
        "Nb_JO_H": len(data["hiver"]),
    })

# Ajout de la ligne TOTAL
resultats.append(total_ligne)

# Tri : d’abord par Nb_JO décroissant, puis par ordre alphabétique.
resultats.sort(key=lambda x: (-x["Nb_JO"], x["délégation"]))

# On affiche le tableau créé.
print(f"{'Délégation':30} | Nb_JO | Nb_JO_E | Nb_JO_H")
print("=-" * 30)
for r in resultats:
    print(f"{r['délégation']:30} | {r['Nb_JO']:5} | {r['Nb_JO_E']:7} | {r['Nb_JO_H']:7}")

finchrono = time.time()
tpsexe = finchrono - debutchrono
print("Le temps d’exécution du programme est de", tpsexe, "seconde(s).")

'''Le programme affiche :
Délégation                     | Nb_JO | Nb_JO_E | Nb_JO_H
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
TOTAL                          |    51 |      29 |      22
France                         |    50 |      29 |      21
USA                            |    50 |      28 |      22
Canada                         |    49 |      27 |      22
Sweden                         |    49 |      27 |      22
Switzerland                    |    49 |      28 |      21
Austria                        |    48 |      26 |      22
Finland                        |    48 |      26 |      22
Norway                         |    47 |      25 |      22
Germany                        |    45 |      25 |      20
Italy                          |    45 |      27 |      18
UK                             |    44 |      29 |      15
Czech Republic                 |    41 |      25 |      16
Netherlands                    |    41 |      26 |      15
Australia                      |    36 |      29 |       7
Russia                         |    34 |      18 |      16
Hungary                        |    33 |      27 |       6
Japan                          |    33 |      21 |      12
Belgium                        |    31 |      27 |       4
Denmark                        |    29 |      28 |       1
Poland                         |    28 |      21 |       7
New Zealand                    |    23 |      22 |       1
South Korea                    |    23 |      16 |       7
Serbia                         |    22 |      20 |       2
Greece                         |    21 |      21 |       0
Mexico                         |    21 |      21 |       0
Spain                          |    21 |      19 |       2
Bulgaria                       |    20 |      16 |       4
Romania                        |    20 |      19 |       1
Argentina                      |    19 |      19 |       0
Brazil                         |    19 |      19 |       0
India                          |    19 |      18 |       1
South Africa                   |    18 |      18 |       0
Turkey                         |    17 |      17 |       0
China                          |    16 |       9 |       7
Iran                           |    16 |      16 |       0
Jamaica                        |    16 |      16 |       0
Cuba                           |    15 |      15 |       0
Ireland                        |    15 |      15 |       0
Portugal                       |    15 |      15 |       0
Estonia                        |    13 |      10 |       3
Belarus                        |    12 |       6 |       6
Ethiopia                       |    12 |      12 |       0
Kenya                          |    12 |      12 |       0
North Korea                    |    12 |      10 |       2
Croatia                        |    11 |       7 |       4
East Germany                   |    11 |       5 |       6
Latvia                         |    11 |       8 |       3
Mongolia                       |    11 |      11 |       0
Slovenia                       |    11 |       7 |       4
Colombia                       |    10 |      10 |       0
Kazakhstan                     |    10 |       6 |       4
Morocco                        |    10 |      10 |       0
Taiwan                         |    10 |      10 |       0
Thailand                       |    10 |      10 |       0
Trinidad                       |    10 |      10 |       0
Ukraine                        |    10 |       6 |       4
Venezuela                      |    10 |      10 |       0
Bahamas                        |     9 |       9 |       0
Egypt                          |     9 |       9 |       0
Nigeria                        |     9 |       9 |       0
Pakistan                       |     9 |       9 |       0
Slovakia                       |     9 |       6 |       3
Indonesia                      |     8 |       8 |       0
Philippines                    |     8 |       8 |       0
Uruguay                        |     8 |       8 |       0
Algeria                        |     7 |       7 |       0
Chile                          |     7 |       7 |       0
Lithuania                      |     7 |       7 |       0
Puerto Rico                    |     7 |       7 |       0
Tunisia                        |     7 |       7 |       0
Uzbekistan                     |     7 |       6 |       1
Azerbaijan                     |     6 |       6 |       0
Georgia                        |     6 |       6 |       0
Israel                         |     6 |       6 |       0
Luxembourg                     |     6 |       5 |       1
Armenia                        |     5 |       5 |       0
Cameroon                       |     5 |       5 |       0
Dominican Republic             |     5 |       5 |       0
Malaysia                       |     5 |       5 |       0
Uganda                         |     5 |       5 |       0
Ghana                          |     4 |       4 |       0
Iceland                        |     4 |       4 |       0
Liechtenstein                  |     4 |       0 |       4
Moldova                        |     4 |       4 |       0
Peru                           |     4 |       4 |       0
Qatar                          |     4 |       4 |       0
Singapore                      |     4 |       4 |       0
Syria                          |     4 |       4 |       0
Costa Rica                     |     3 |       3 |       0
Haiti                          |     3 |       3 |       0
Hong Kong                      |     3 |       3 |       0
Lebanon                        |     3 |       3 |       0
Tajikistan                     |     3 |       3 |       0
Vietnam                        |     3 |       3 |       0
Zimbabwe                       |     3 |       3 |       0
Afghanistan                    |     2 |       2 |       0
Bahrain                        |     2 |       2 |       0
Burundi                        |     2 |       2 |       0
Ecuador                        |     2 |       2 |       0
Grenada                        |     2 |       2 |       0
Individual Olympic Athletes    |     2 |       2 |       0
Ivory Coast                    |     2 |       2 |       0
Kuwait                         |     2 |       2 |       0
Kyrgyzstan                     |     2 |       2 |       0
Mozambique                     |     2 |       2 |       0
Namibia                        |     2 |       2 |       0
Niger                          |     2 |       2 |       0
Panama                         |     2 |       2 |       0
Saudi Arabia                   |     2 |       2 |       0
Sri Lanka                      |     2 |       2 |       0
Suriname                       |     2 |       2 |       0
United Arab Emirates           |     2 |       2 |       0
Zambia                         |     2 |       2 |       0
Barbados                       |     1 |       1 |       0
Bermuda                        |     1 |       1 |       0
Botswana                       |     1 |       1 |       0
Curacao                        |     1 |       1 |       0
Cyprus                         |     1 |       1 |       0
Djibouti                       |     1 |       1 |       0
Eritrea                        |     1 |       1 |       0
Fiji                           |     1 |       1 |       0
Gabon                          |     1 |       1 |       0
Guatemala                      |     1 |       1 |       0
Guyana                         |     1 |       1 |       0
Iraq                           |     1 |       1 |       0
Jordan                         |     1 |       1 |       0
Kosovo                         |     1 |       1 |       0
Macedonia                      |     1 |       1 |       0
Mauritius                      |     1 |       1 |       0
Monaco                         |     1 |       1 |       0
Montenegro                     |     1 |       1 |       0
Nepal                          |     1 |       0 |       1
Paraguay                       |     1 |       1 |       0
Senegal                        |     1 |       1 |       0
Sudan                          |     1 |       1 |       0
Tanzania                       |     1 |       1 |       0
Togo                           |     1 |       1 |       0
Tonga                          |     1 |       1 |       0
Virgin Islands, US             |     1 |       1 |       0
Le temps d’exécution est de 2.339852809906006 secondes.'''
