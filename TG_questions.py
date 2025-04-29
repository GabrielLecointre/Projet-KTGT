# question : combien de sportifs ont changé de délégation ?

import pandas as pd

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv")

# Exclure les entrées "IOA", athlètes neutres
donnees1 = donnees[donnees["NOC"] != "IOA"]

# Compter le nombre de modalités distinctes de NOC pour chaque valeur de ID
multi_noc = donnees1.groupby('ID')['NOC'].nunique()

# Garder les valeurs de ID où NOC a plus d'une modalité
id_with_multiple_noc = multi_noc[multi_noc > 1].index

# Filtrer le DataFrame original
filtered_donnees = donnees1[donnees1['ID'].isin(id_with_multiple_noc)]

print(filtered_donnees)

filtered_donnees.to_csv('filtered_donnees.csv', sep=';', encoding='utf-8', index=False)

print(f"Nb de sportifs ayant représenté plusieurs pays : {len(id_with_multiple_noc)}")

# question : combien de sports sont concernés ?

# Pour ces IDs, lister et compter les sports concernés
sports_for_these_ids = donnees1[donnees1['ID'].isin(id_with_multiple_noc)]['Sport']
sports_count = sports_for_these_ids.value_counts()

print("\nSports pratiqués par les IDs présents dans plusieurs pays :")
print(sports_count)

sports_count.to_csv('sports_count.csv', sep=';', encoding='utf-8', index=True)

print(f"\nNombre total de modalités de sports concernées : {len(sports_count)}")

# question : quel sport compte le plus de sportifs concernés ?

sport_max = sports_count.idxmax()
valeur_max = sports_count.max()
print(f"Sport le plus fréquent: {sport_max} ({valeur_max} occurrences)")

