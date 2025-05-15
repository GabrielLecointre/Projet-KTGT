# Quels ont été les résultats spécifiques de Nadia Comăneci lors des JO de 1976?

import pandas as pd
import re

# Lire le fichier CSV
donnees = pd.read_csv("athlete_events.csv")

# pour éviter de filtrer directement sur 1976 et sur Nadia Comăneci
# Demander à l'utilisateur d'indiquer l'année et le sportif
nom_sportif = input("Entrez le nom du sportif pour afficher ses résultats : ").lower()
annee = int(input("Entrez l'année des Jeux Olympiques : "))

# dans la base de données les caractères spéciaux ont été soit remplacés soit supprimés
# Filtrer sur le nom (recherche partielle, insensible à la casse)
# filtre_nom = donnees["Name"].str.lower().str.contains(nom_sportif)

# Transformer la saisie en mots-clés séparés
mots = nom_sportif.strip().lower().split()

# Construire l'expression régulière : chaque mot doit apparaître, peu importe l’ordre
pattern = ''.join(f'(?=.*{re.escape(mot)})' for mot in mots)

# Appliquer le filtre avec regex=True et case=False
filtre_nom = donnees["Name"].str.lower().str.contains(pattern, regex=True)
sportif = donnees[filtre_nom]

# Vérifier si des données existent
if sportif.empty:
    print("Aucun sportif trouvé avec ce nom.")
else:
    # Filtrer sur l'année souhaitée
    sportif_annee = sportif[sportif["Year"] == annee]

    if sportif_annee.empty:
        print(f"Aucune participation trouvée en {annee} pour ce sportif.")
    else:
        # Préparer les données pour l'export Excel
        data_export = sportif_annee[["Year", "Name", "Event", "Medal"]]
        data_export.columns = ["Année", "Nom", "Épreuve", "Médaille"]

        # Générer un nom de fichier propre
        nom_fichier_excel = f"resultats_{nom_sportif.replace(' ', '_')}_{annee}.xlsx"

        # Exporter vers Excel
        data_export.to_excel(nom_fichier_excel, index=False)

        # Afficher les résultats
        print(f"Résultats pour {data_export['Nom'].iloc[0]} en {annee} :")
        for index, row in data_export.iterrows():
            print(f"Épreuve: {row['Épreuve']}")
            print(f"Médaille: {row['Médaille']}")
            print("-" * 30)
