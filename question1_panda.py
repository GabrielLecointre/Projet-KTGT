import pandas as pd

# Charger les données
df = pd.read_csv('donnees_jeux_olympiques/athlete_events.csv')

# nom de l'athlète
nom = "michael fred"

# Ne conserver que les colonnes d'intérêt
donnees = df[['Year', 'Name', 'Event', 'Medal']]

# Filtrer par nom insensible à la casse
donnees_nom = donnees[donnees['Name'].str.lower().str.contains(nom.lower())]

# Compter le nombre de médailles par type
medailles_count = donnees_nom['Medal'].value_counts()

# Calculer le total des médailles (en excluant les valeurs None)
total_medailles = medailles_count.sum()

print(f"Total des médailles: {total_medailles}")
print(medailles_count)
