import pandas
import os

# Lire le fichier .csv avec la base de données
BDJO = pandas.read_csv(os.path.join("donnees_jeux_olympiques", "athlete_events.csv"))
print("* Tableau du fichier :")
print(BDJO)
