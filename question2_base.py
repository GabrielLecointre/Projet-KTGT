import csv

# Lire le fichier CSV avec la librairie csv
with open('donnees_jeux_olympiques/athlete_events.csv', 'r', encoding='utf-8') as donnees:
    lecteur = csv.reader(donnees)
    tableau = list(lecteur)  # Convertir en liste de listes

# Extraire seulement les infos nécessaires : Team, Year ,Event, Medal
medaille_nation = []
for ligne in tableau:
    nouvelle_ligne = [ligne[6], ligne[9], ligne[13], ligne[14]]  # Team (6), Year (9), Event (13), Medal (14)
    medaille_nation.append(nouvelle_ligne)

# Supprimer les doublons
# chaque joueur d''une équipe reçoit une médaille par épreuve
# Or, on ne comptabilise qu'une médaille par équipe et par épreuve pour un pays
# on conserve qu'une médaille par équipe et par épreuve
medaille_nation_sans_doublons = [list(t) for t in set(tuple(l) for l in medaille_nation)]

# print(len(medaille_nation))  # Total des lignes
# print(len(medaille_nation_sans_doublons))  # Total après suppression des doublons

# fonction qui comptabilise le nombre de médailles par pays et par année
def compter_medailles_par_pays(annee):
    # Initialisation du dictionnaire de résultat
    resultat = {}

    # Filtrer les médailles pour l'année donnée
    for ligne in medaille_nation_sans_doublons:
        team, year, event, medal = ligne

        # Si l'année correspond, on compte la médaille
        if year == str(annee):
            if team not in resultat:
                resultat[team] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
            if medal == 'Gold':
                resultat[team]['Gold'] += 1
            elif medal == 'Silver':
                resultat[team]['Silver'] += 1
            elif medal == 'Bronze':
                resultat[team]['Bronze'] += 1

    # Calculer le total de médailles pour chaque pays
    for pays, medailles in resultat.items():
        total_medaille = medailles['Gold'] + medailles['Silver'] + medailles['Bronze']
        medailles['Total'] = total_medaille

    # Trier les résultats par total de médailles en ordre croissant
    resultat_trie = sorted(resultat.items(), key=lambda x: x[1]['Total'], reverse=True)

    # Affichage du résultat trié
    for pays, medailles in resultat_trie:
        print(f"{pays} : Gold={medailles['Gold']}, Silver={medailles['Silver']}, Bronze={medailles['Bronze']}, Total={medailles['Total']}")


# Exemple d'appel de la fonction pour l'année 2016
compter_medailles_par_pays(2016)
