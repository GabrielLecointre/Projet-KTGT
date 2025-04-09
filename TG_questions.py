import pandas as pd

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv")

# question : quel sportif a participé au plus d'épreuves sans jamais être médaillé ?

# Filtrer les données pour garder uniquement les athletes avec médailles
donnees2 = donnees.dropna(subset=["Medal"])  # supprimer les valeurs manquantes
donnees2 = donnees2[donnees2["Medal"] != "NA"]  # Exclure les entrées "NA"

# Filtrer les données pour garder uniquement les athletes sans médailles
donnees3 = donnees[donnees["Medal"] != "Gold"]  # Exclure les entrées "Gold"
donnees3 = donnees3[donnees3["Medal"] != "Silver"]  # Exclure les entrées "Silver"
donnees3 = donnees3[donnees3["Medal"] != "Bronze"]  # Exclure les entrées "Bronze"

# conserver uniquement les athletes qui n'ont jamais eu de médaille
donnees4 = pd.merge(
    donnees3, donnees2, how='outer', on='ID', indicator=True).query(
        '_merge=="left_only"').drop(columns='_merge')

print(donnees4)

# trier les ID par nombre de participations


compte = donnees4['ID'].value_counts(dropna=False).reset_index()
print(compte)
compte.to_csv('compte.csv', sep=';', encoding='utf-8', index=False)
donnees4.to_csv('donnees4.csv', sep=';', encoding='utf-8', index=False)
