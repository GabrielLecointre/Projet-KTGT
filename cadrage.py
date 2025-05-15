import pandas as pd

# Charger les données (remplace "athletes.csv" par le nom réel de ton fichier)
# Lire le fichier CSV
df = pd.read_csv("athlete_events.csv")

# On filtre pour ne garder que les Jeux d'été
df_ete = df[df["Season"] == "Summer"]


# Fonction pour obtenir les données de cadrage pour une année donnée
def cadrage_annee(df, annee):
    df_annee = df[df["Year"] == annee]
    nb_sportifs = df_annee["ID"].nunique()
    nb_sports = df_annee["Sport"].nunique()
    nb_delegations = df_annee["NOC"].nunique()
    return nb_sportifs, nb_sports, nb_delegations


# Données pour 1896
sportifs_1896, sports_1896, delegations_1896 = cadrage_annee(df_ete, 1896)

# Données pour 2016
sportifs_2016, sports_2016, delegations_2016 = cadrage_annee(df_ete, 2016)

# Affichage des résultats
print("### Jeux d'été 1896 ###")
print(f"Nombre de sportifs : {sportifs_1896}")
print(f"Nombre de sports : {sports_1896}")
print(f"Nombre de délégations : {delegations_1896}")

print("\n### Jeux d'été 2016 ###")
print(f"Nombre de sportifs : {sportifs_2016}")
print(f"Nombre de sports : {sports_2016}")
print(f"Nombre de délégations : {delegations_2016}")
