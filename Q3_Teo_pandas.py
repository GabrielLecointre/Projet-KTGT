# Quels ont été les résultats spécifiques de Nadia Comăneci lors des JO de 1976?

import pandas as pd

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv")

# Filtrer les données pour Nadia Comăneci
nadia = donnees[donnees["Name"] == "Nadia Elena Comneci (-Conner)"]

# Filtrer les données pour l'année 1976
nadia_1976 = nadia[nadia["Year"] == 1976]

# Préparer les données pour l'export Excel
data_export = nadia_1976[["Year", "Name", "Event", "Medal"]]
data_export.columns = ["Année", "Nom", "Épreuve", "Médaille"]  # Renommer les colonnes

# Exporter les résultats vers un fichier Excel
nom_fichier_excel = "resultats_nadia_comaneci_1976.xlsx"
data_export.to_excel(nom_fichier_excel, index=False)

# Afficher les résultats spécifiques de Nadia Comăneci en 1976
print("Résultats de Nadia Comăneci aux Jeux Olympiques de 1976 :")
for index, row in nadia_1976.iterrows():
    print(f"Épreuve: {row['Event']}")
    print(f"Médaille: {row['Medal']}")
    print("-" * 30)
