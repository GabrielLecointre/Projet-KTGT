import pandas as pd

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv", usecols=['ID', 'Name', 'Medal'])

<<<<<<< HEAD
=======
# question : quel sportif a participé au plus d'épreuves sans jamais être médaillé ?

# Filtrer les données pour garder uniquement les athletes avec médailles
donnees2 = donnees.dropna(subset=["Medal"])  # supprimer les valeurs manquantes
donnees2 = donnees2[donnees2["Medal"] != "NA"]  # Exclure les entrées "NA"
>>>>>>> 67bd888d6c57baef1aef34f1409483eb324c7fa1

# question : quel sportif a participé au plus d'épreuves sans jamais être médaillé ?


# Séparer les données en fonction de la médaille
donnees_medaille = donnees[donnees['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
donnees_autre = donnees[~donnees['Medal'].isin(['Gold', 'Silver', 'Bronze'])]

# conserver uniquement les athletes qui n'ont jamais eu de médaille
<<<<<<< HEAD
donnees_sans_only = pd.merge(
    donnees_autre, donnees_medaille, how='outer', on='ID', indicator=True).query(
        '_merge=="left_only"').drop(columns='_merge')


# trier les ID par nombre de participations

# Compter les occurrences des modalités de la variable 'ID'
# modalites_count = donnees2['Name'].value_counts()

# Obtenir la modalité la plus fréquente et son nombre d'apparitions
# top_modalite = modalites_count.idxmax('Name')  # La modalité la plus fréquente
# top_modalite_count = modalites_count.max('Name')  # Le nombre d'apparitions de la
# modalité

# Créer un DataFrame avec ces informations
# top_modalite_df = pd.DataFrame({
#    'Modalite': [top_modalite],
#    'Count': [top_modalite_count]
# })

# Exporter le résultat dans un fichier CSV
# top_modalite_df.to_csv('modalite_plus_frequente.csv', sep=';', encoding='utf-8',
#                        index=False)

# Compter les occurrences des modalités de la variable 'ID' avec groupby() et size()
modalites_count = donnees_sans_only.groupby('Name').size()

# Obtenir la modalité la plus fréquente et son nombre d'apparitions
top_modalite = modalites_count.idxmax()  # La modalité la plus fréquente
top_modalite_count = modalites_count.max()  # Le nombre d'apparitions de la modalité

# Créer un DataFrame avec ces informations
modalite_plus_frequente = pd.DataFrame({
    'Modalite': [top_modalite],
    'Count': [top_modalite_count]
})

# Exporter le résultat dans un fichier CSV
modalite_plus_frequente.to_csv('modalite_plus_frequente.csv', index=False)

compte = donnees_sans_only['ID'].value_counts(dropna=False).reset_index()
print(compte)
compte.to_csv('compte.csv', sep=';', encoding='utf-8', index=False)
donnees_sans_only.to_csv('donnees2.csv', sep=';', encoding='utf-8', index=False)


#################################################################################


# conserver uniquement les athletes qui n'ont jamais eu de médaille
donnees5 = pd.merge(
    donnees_autre, donnees_medaille, how='outer', on='ID', indicator=True).query(
        '_merge=="left_only"').drop(columns='_merge')


# Compter les occurrences de chaque ID
occurrences = donnees5['ID'].value_counts(dropna=False)


# Extraire les 10 ID les plus fréquents
top_10_id = occurrences.head(10).index


# Filtrer les lignes du DataFrame pour ne garder que celles qui ont les 10 ID
# les plus fréquents
donnees_top_10 = donnees5[donnees5['ID'].isin(top_10_id)]

# Exporter le résultat dans un fichier CSV
donnees_top_10.to_csv('top_10_id.csv', sep=';', encoding='utf-8', index=False)

=======
donnees4 = pd.merge(
    donnees3, donnees2, how='outer', on='ID', indicator=True).query(
        '_merge=="left_only"').drop(columns='_merge')

print(donnees4)
>>>>>>> 67bd888d6c57baef1aef34f1409483eb324c7fa1

# trier les ID par nombre de participations


<<<<<<< HEAD
compte = donnees_sans_only['ID'].value_counts(dropna=False).reset_index()
print(compte)
compte.to_csv('compte.csv', sep=';', encoding='utf-8', index=False)
donnees_sans_only.to_csv('donnees2.csv', sep=';', encoding='utf-8', index=False)
=======
compte = donnees4['ID'].value_counts(dropna=False).reset_index()
print(compte)
compte.to_csv('compte.csv', sep=';', encoding='utf-8', index=False)
donnees4.to_csv('donnees4.csv', sep=';', encoding='utf-8', index=False)
>>>>>>> 67bd888d6c57baef1aef34f1409483eb324c7fa1
