import pandas as pd

# Charger les données
donnees = pd.read_csv("athlete_events.csv")

# 1) Classification des épreuves sportives pour une année donnée


def classifier_epreuves(df, annee):
    df_annee = df[df["Year"] == annee]

    def get_type_epreuve(group):
        if group["Event"].nunique() > 1:
            return "Combinée"
        medal_counts = group["Medal"].value_counts().sum()
        if medal_counts >= 6:
            return "Collective (estimation)"
        else:
            return "Individuelle"

    classification = (
        df_annee.groupby("Event")
        .agg(
            nombre_epreuves_dans_sport=("Sport", "nunique"),
            part_femmes_participants=(
                "Sex",
                lambda x: (x == "F").sum() / len(x) if len(x) > 0 else 0,
            ),
            nombre_participants=("ID", "nunique"),
            nombre_pays_participant=("NOC", "nunique"),
            age_moyen_participants=("Age", "mean"),
            ecart_type_age_athletes=("Age", "std"),
            poids_moyen_athletes=("Weight", "mean"),
            ecart_type_poids_athletes=("Weight", "std"),
            taille_moyenne_athletes=("Height", "mean"),
            ecart_type_taille_athletes=("Height", "std"),
            annee_apparition_epreuve=("Year", "min"),
            type_epreuve=("", get_type_epreuve),
        )
        .reset_index()
    )

    return classification


# Exemple de classification pour l'année 2016
annee_cible_1 = 2016
classification_2016 = classifier_epreuves(donnees, annee_cible_1)
print(
    f"\nClassification des épreuves sportives pour l'année {annee_cible_1}:"
    f"\n{classification_2016}"
)

# 2) Comparaison de la classification sur 4 périodes couvrant 100 ans


def comparer_classifications(df, periode_debut, taille_periode=25):
    classifications_par_periode = {}
    for i in range(4):
        annee_debut = periode_debut + i * taille_periode
        annee_fin = annee_debut + taille_periode - 1
        annee_milieu = (
            annee_debut + annee_fin
        ) // 2  # Choisir une année représentative
        df_periode = df[(df["Year"] >= annee_debut) & (df["Year"] <= annee_fin)]
        if not df_periode.empty:
            classification = classifier_epreuves(df_periode, annee_milieu)
            classifications_par_periode[f"{annee_debut}-{annee_fin}"] = classification
        else:
            classifications_par_periode[f"{annee_debut}-{annee_fin}"] = pd.DataFrame()
            print(f"Aucune donnée trouvée pour la période {annee_debut}-{annee_fin}.")
    return classifications_par_periode


# Comparaison sur 4 périodes de 25 ans commençant en 1920 (pour couvrir environ 100 ans)
periode_debut_comparaison = 1920
classifications_historiques = comparer_classifications(
    donnees, periode_debut_comparaison
)

print("\nComparaison de la classification des épreuves sur différentes périodes:")
for periode, classification in classifications_historiques.items():
    print(f"\n--- Période: {periode} ---")
    if not classification.empty:
        print(
            classification.head()
        )  # Afficher les premières lignes pour chaque période
    else:
        print("Aucune donnée de classification pour cette période.")

# Analyse de l'évolution (à compléter)
print("\nAnalyse de l'évolution des groupes d'épreuves au cours du dernier siècle:")
# Ici, vous pouvez comparer les classifications des différentes périodes pour identifier
# des tendances dans les caractéristiques physiques des athlètes et la formation des
# groupes d'épreuves.
# Par exemple, vous pourriez comparer l'évolution de la taille moyenne des athlètes
# dans certains sports ou la part des femmes participantes au fil du temps.


# Adaptation de la fonction correct_medal_counts pour le type d'épreuve
def determiner_type_epreuve_v2(df):
    def get_type(group):
        medal_counts = group["Medal"].value_counts().sum()
        return "Collective" if medal_counts >= 6 else "Individuelle"

    type_epreuve = (
        df.groupby("Event").apply(get_type).reset_index(name="type_epreuve_v2")
    )
    df_merged = pd.merge(df, type_epreuve, on="Event", how="left")
    return df_merged


donnees_avec_type = determiner_type_epreuve_v2(donnees)
print(
    "\nDonnées avec le type d'épreuve déterminé :\n",
    donnees_avec_type[["Event", "Medal", "type_epreuve_v2"]].head(),
)

# Pour intégrer cette logique dans la classification initiale, vous pouvez modifier
# la fonction classifier_epreuves.


# Exemple d'intégration dans classifier_epreuves:
def classifier_epreuves_integre(df, annee):
    df_annee = df[df["Year"] == annee].copy()

    def get_type_epreuve_integre(group):
        if group["Event"].nunique() > 1:
            return "Combinée"
        medal_counts = group["Medal"].value_counts().sum()
        if medal_counts >= 6:
            return "Collective"
        else:
            return "Individuelle"

    classification = (
        df_annee.groupby("Event")
        .agg(
            nombre_epreuves_dans_sport=("Sport", "nunique"),
            part_femmes_participants=(
                "Sex",
                lambda x: (x == "F").sum() / len(x) if len(x) > 0 else 0,
            ),
            nombre_participants=("ID", "nunique"),
            nombre_pays_participant=("NOC", "nunique"),
            age_moyen_participants=("Age", "mean"),
            ecart_type_age_athletes=("Age", "std"),
            poids_moyen_athletes=("Weight", "mean"),
            ecart_type_poids_athletes=("Weight", "std"),
            taille_moyenne_athletes=("Height", "mean"),
            ecart_type_taille_athletes=("Height", "std"),
            annee_apparition_epreuve=("Year", "min"),
            type_epreuve=("", get_type_epreuve_integre),
        )
        .reset_index()
    )

    return classification


annee_cible_integre = 2016
classification_2016_integre = classifier_epreuves_integre(donnees, annee_cible_integre)
print(
    f"\nClassification des épreuves sportives pour l'année {annee_cible_integre}:"
    f"\n{classification_2016_integre}"
)

# Pour répondre à la problématique, vous devrez analyser les résultats de la
# comparaison des classifications au fil du temps. Examinez comment les
# caractéristiques physiques moyennes et la diversité des athlètes évoluent
# pour différents types d'épreuves (individuelles, collectives, combinées)
# au cours des différentes périodes.

# Par exemple, vous pourriez visualiser l'évolution de la taille moyenne des
# athlètes dans les épreuves collectives par rapport aux épreuves individuelles.
# Vous pourriez également examiner comment la part des femmes participantes
# a changé dans différents types d'épreuves.

# N'hésitez pas à poser d'autres questions si vous avez besoin d'aide pour des
# analyses ou visualisations spécifiques.
