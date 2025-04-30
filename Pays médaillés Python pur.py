# Ce programme en Python pur donne les pays qui ont été médaillés
# dans le maximum d’éditions différentes des Jeux Olympiques.
# ATTENTION : CHANGER LE CHEMIN DU FICHIER SI BESOIN
import csv
import os

# --- Étape 1 : Chargement des fichiers CSV ---

# Adapter le chemin si nécessaire
chemin_base = "donnees_jeux_olympiques"
BDJO = os.path.join(chemin_base, "athlete_events.csv")
pays = os.path.join(chemin_base, "noc_regions.csv")

# Chargement des NOC vers régions
noc_to_region = {}
with open(pays, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        noc = row["NOC"]
        region = row["region"]
        noc_to_region[noc] = region

# Corrections manuelles
corrections = {
    "SGP": "Singapore",
    "HKG": "Hong Kong",
    "WIF": "Jamaica",
    "GDR": "East Germany",
}
noc_to_region.update(corrections)

# Dictionnaire pour stocker les éditions avec médailles par pays
noc_games = {}  # clé : NOC, valeur : set de Games
noc_ete = {}    # clé : NOC, valeur : set de Games d'été
noc_hiver = {}  # clé : NOC, valeur : set de Games d'hiver

# Pour connaître le nombre total d'éditions (été/hiver)
total_games = set()
ete_games = set()
hiver_games = set()

with open(BDJO, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["Medal"] not in {"Gold", "Silver", "Bronze"}:
            continue  # On ignore les lignes sans médaille

        noc = row["NOC"]
        games = row["Games"]
        season = row["Season"]

        total_games.add(games)
        if season == "Summer":
            ete_games.add(games)
        else:
            hiver_games.add(games)

        # Initialisation des sets si nécessaires
        if noc not in noc_games:
            noc_games[noc] = set()
            noc_ete[noc] = set()
            noc_hiver[noc] = set()

        noc_games[noc].add(games)
        if season == "Summer":
            noc_ete[noc].add(games)
        else:
            noc_hiver[noc].add(games)

# --- Étape 2 : Regroupement des pays historiques ---

# Dictionnaire final : région → sets d’éditions
region_data = {}

# Regroupements historiques
regroupements = {
    "ANZ": "Australia",
    "BOH": "Czech Republic",
    "TCH": "Czech Republic",
    "YUG": "Serbia",
    "SCG": "Serbia",
    "URS": "Russia",
    "EUN": "Russia",
    "FRG": "Germany",
    "WIF": "Jamaica",  # redondant avec correction plus haut
}

for noc in noc_games:
    region = regroupements.get(noc, noc_to_region.get(noc, noc))  # fallback : NOC si pas trouvé

    if region not in region_data:
        region_data[region] = {
            "total": set(),
            "ete": set(),
            "hiver": set()
        }

    region_data[region]["total"].update(noc_games[noc])
    region_data[region]["ete"].update(noc_ete[noc])
    region_data[region]["hiver"].update(noc_hiver[noc])

# --- Étape 3 : Création du tableau final ---

# Calcul ligne "TOTAL"
total_ligne = {
    "délégation": "TOTAL",
    "Nb_JO": len(total_games),
    "Nb_JO_E": len(ete_games),
    "Nb_JO_H": len(hiver_games),
}

# Liste des résultats par pays
resultats = []

for region, data in region_data.items():
    resultats.append({
        "délégation": region,
        "Nb_JO": len(data["total"]),
        "Nb_JO_E": len(data["ete"]),
        "Nb_JO_H": len(data["hiver"]),
    })

# Ajout de la ligne TOTAL
resultats.append(total_ligne)

# Tri : d'abord par Nb_JO décroissant, puis par ordre alphabétique
resultats.sort(key=lambda x: (-x["Nb_JO"], x["délégation"]))

# --- Étape 4 : Affichage ---

print(f"{'Délégation':30} | Nb_JO | Nb_JO_E | Nb_JO_H")
print("-" * 60)
for r in resultats:
    print(f"{r['délégation']:30} | {r['Nb_JO']:6} | {r['Nb_JO_E']:8} | {r['Nb_JO_H']:8}")
