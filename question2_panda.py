import pandas as pd

# Charger les données
df = pd.read_csv('donnees_jeux_olympiques/athlete_events.csv')

# Ne conserver que les colonnes d'intérêt et filtrer pour 2016
donnees = df[['Team', 'Year', 'Event', 'Medal']]
donnees_2016 = donnees[donnees['Year'] == 2016]

# --------- Borne supérieure (avec doublons) ---------
medailles_sup = donnees_2016.groupby(['Team', 'Medal']).size().unstack(fill_value=0)
medailles_sup['Total_sup'] = medailles_sup.sum(axis=1)

# --------- Borne inférieure (sans doublons) ---------
donnees_sans_doublons = donnees_2016.drop_duplicates(subset=['Team', 'Event', 'Medal'])
medailles_inf = donnees_sans_doublons.groupby(['Team', 'Medal']).size().unstack(fill_value=0)
medailles_inf['Total_inf'] = medailles_inf.sum(axis=1)

# --------- Fusion des deux jeux de données ---------
# Renommer les colonnes pour les bornes inf et sup
medailles_inf = medailles_inf.rename(columns={
    'Gold': 'Gold_inf',
    'Silver': 'Silver_inf',
    'Bronze': 'Bronze_inf'
})
medailles_sup = medailles_sup.rename(columns={
    'Gold': 'Gold_sup',
    'Silver': 'Silver_sup',
    'Bronze': 'Bronze_sup'
})

# Fusionner sur 'Team'
resultat = pd.merge(medailles_inf, medailles_sup, left_index=True, right_index=True, how='outer')
resultat = resultat.fillna(0).astype(int)

# Trier par total des médailles supérieures décroissant
resultat = resultat.sort_values(by='Total_sup', ascending=False)

print(resultat)
