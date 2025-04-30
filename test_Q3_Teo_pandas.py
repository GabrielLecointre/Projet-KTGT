import pandas as pd


def test_resultats_nadia_comaneci_1976():
    # Charger les données
    donnees = pd.read_csv("athlete_events.csv")

    # Filtrer Nadia Comăneci (recherche tolérante, insensible à la casse)
    filtre_nom = donnees["Name"].str.lower().str.contains("comaneci")
    nadia = donnees[filtre_nom]
    nadia_1976 = nadia[nadia["Year"] == 1976]

    # Liste des résultats attendus sous forme de tuples (épreuve, médaille)
    attendus = [
        ("Gymnastics Women's Individual All-Around", "Gold"),
        ("Gymnastics Women's Team All-Around", "Silver"),
        ("Gymnastics Women's Floor Exercise", "Bronze"),
        ("Gymnastics Women's Horse Vault", None),  # Pas de médaille
        ("Gymnastics Women's Uneven Bars", "Gold"),
        ("Gymnastics Women's Balance Beam", "Gold"),
    ]

    # Vérifier que chaque couple (épreuve, médaille) est présent dans les données
    for epreuve_attendue, medaille_attendue in attendus:
        lignes = nadia_1976[nadia_1976["Event"] == epreuve_attendue]
        assert not lignes.empty, f"{epreuve_attendue} absente des résultats"
        medals = lignes["Medal"].tolist()
        if medaille_attendue is None:
            assert any(
                pd.isna(m) for m in medals
            ), f"{epreuve_attendue} devrait être sans médaille"
        else:
            assert (
                medaille_attendue in medals
            ), f"{epreuve_attendue} : médaille {medaille_attendue} non trouvée"
