# Ce programme en Python pur donne les pays qui ont été médaillés
# dans le maximum d’éditions différentes des Jeux Olympiques.
# ATTENTION : CHANGER LE CHEMIN DU FICHIER SI BESOIN
import csv
import os

# On charge les fichiers.
chemin_base = "donnees_jeux_olympiques"
BDJO = os.path.join(chemin_base, "athlete_events.csv")
pays = os.path.join(chemin_base, "noc_regions.csv")

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
        if saison == "Summer": # Jeux d’été
            e_JO.add(jeux)
        else: # Forcément "Winter" pour ceux d’hiver.
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

# Tri : d'abord par Nb_JO décroissant, puis par ordre alphabétique
resultats.sort(key=lambda x: (-x["Nb_JO"], x["délégation"]))

# On affiche le tableau créé.
print(f"{'Délégation':30} | Nb_JO | Nb_JO_E | Nb_JO_H")
print("=-" * 30)
for r in resultats:
    print(f"{r['délégation']:30} | {r['Nb_JO']:5} | {r['Nb_JO_E']:7} | {r['Nb_JO_H']:7}")
