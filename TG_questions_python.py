import csv
from collections import defaultdict, Counter

# Lire le fichier CSV


def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

# Lire les données


donnees = read_csv("athlete_events.csv")

# question : combien de sportifs ont changé de délégation ?

# Exclure les entrées "IOA", athlètes neutres
donnees1 = [row for row in donnees if row["NOC"] != "IOA"]

# Compter le nombre de modalités distinctes de NOC pour chaque valeur de ID
noc_by_id = defaultdict(set)
for row in donnees1:
    noc_by_id[row['ID']].add(row['NOC'])

# Garder les valeurs de ID où NOC a plus d'une modalité
id_with_multiple_noc = [id for id, nocs in noc_by_id.items() if len(nocs) > 1]

# Filtrer les données
filtered_donnees = [row for row in donnees1 if row['ID'] in id_with_multiple_noc]

# Exporter les données filtrées
with open('filtered_donnees.csv', 'w', encoding='utf-8', newline='') as file:
    fieldnames = filtered_donnees[0].keys() if filtered_donnees else []
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(filtered_donnees)

# Afficher le nombre de sportifs concernés
print(f"Nb de sportifs ayant représenté plusieurs pays : {len(id_with_multiple_noc)}")
# résultat attendu : Nb de sportifs ayant représenté plusieurs pays : 1537

# question : combien de sports sont concernés ?

# Compter les sports concernés
sports_for_these_ids = [row['Sport'] for row in donnees1
                        if row['ID'] in id_with_multiple_noc]
sports_count = Counter(sports_for_these_ids)

# Afficher les sports
print("\nSports pratiqués par les IDs présents dans plusieurs pays :")
for sport, count in sports_count.items():
    print(f"{sport}: {count}")

# Exporter les comptages de sports
with open('sports_count.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Sport', 'Count'])
    writer.writerows(sports_count.items())

# Afficher le nombre total de sports concernés
print(f"\nNombre total de modalités de sports concernées : {len(sports_count)}")
# résultat attendu : Nombre total de modalités de sports concernées : 47

# question : quel sport compte le plus de sportifs concernés ?
sport_max = max(sports_count.items(), key=lambda x: x[1])
print(f"Sport le plus fréquent: {sport_max[0]} ({sport_max[1]} occurrences)")
# résultat attendu : Sport le plus fréquent: Athletics (862 occurrences)
