import pandas as pd
import pytest
from Q1_Teo_pandas import trouver_athletes_ete_hiver


# Créer un petit ensemble de données de test
@pytest.fixture
def donnees_test():
    data = [
        # Eddie Eagan
        {
            "ID": 31167,
            "Name": 'Edward Patrick Francis "Eddie" Eagan',
            "Sex": "M",
            "Age": 32,
            "Season": "Summer",
            "Year": 1920,
            "Sport": "Boxing",
            "Medal": "Gold",
        },
        {
            "ID": 31167,
            "Name": 'Edward Patrick Francis "Eddie" Eagan',
            "Sex": "M",
            "Age": 44,
            "Season": "Winter",
            "Year": 1932,
            "Sport": "Bobsleigh",
            "Medal": "Gold",
        },
        # Clara Hughes
        {
            "ID": 50859,
            "Name": "Clara Hughes",
            "Sex": "F",
            "Age": 24,
            "Season": "Summer",
            "Year": 1996,
            "Sport": "Cycling",
            "Medal": "Bronze",
        },
        {
            "ID": 50859,
            "Name": "Clara Hughes",
            "Sex": "F",
            "Age": 30,
            "Season": "Winter",
            "Year": 2002,
            "Sport": "Speed Skating",
            "Medal": "Bronze",
        },
        {
            "ID": 50859,
            "Name": "Clara Hughes",
            "Sex": "F",
            "Age": 34,
            "Season": "Winter",
            "Year": 2006,
            "Sport": "Speed Skating",
            "Medal": "Silver",
        },
        # Christa Rothenburger-Luding
        {
            "ID": 102862,
            "Name": "Christa Rothenburger-Luding",
            "Sex": "F",
            "Age": 23,
            "Season": "Winter",
            "Year": 1984,
            "Sport": "Speed Skating",
            "Medal": "Gold",
        },
        {
            "ID": 102862,
            "Name": "Christa Rothenburger-Luding",
            "Sex": "F",
            "Age": 27,
            "Season": "Winter",
            "Year": 1988,
            "Sport": "Speed Skating",
            "Medal": "Silver",
        },
        {
            "ID": 102862,
            "Name": "Christa Rothenburger-Luding",
            "Sex": "F",
            "Age": 27,
            "Season": "Summer",
            "Year": 1988,
            "Sport": "Cycling",
            "Medal": "Silver",
        },
        {
            "ID": 102862,
            "Name": "Christa Rothenburger-Luding",
            "Sex": "F",
            "Age": 27,
            "Season": "Winter",
            "Year": 1988,
            "Sport": "Speed Skating",
            "Medal": "Gold",
        },
        {
            "ID": 102862,
            "Name": "Christa Rothenburger-Luding",
            "Sex": "F",
            "Age": 31,
            "Season": "Winter",
            "Year": 1992,
            "Sport": "Speed Skating",
            "Medal": "Silver",
        },
        # Jacob Thams
        {
            "ID": 119489,
            "Name": "Jacob Tullin Thams",
            "Sex": "M",
            "Age": 26,
            "Season": "Winter",
            "Year": 1924,
            "Sport": "Ski Jumping",
            "Medal": "Gold",
        },
        {
            "ID": 119489,
            "Name": "Jacob Tullin Thams",
            "Sex": "M",
            "Age": 38,
            "Season": "Summer",
            "Year": 1936,
            "Sport": "Sailing",
            "Medal": "Silver",
        },
        # Lauryn Williams
        {
            "ID": 130626,
            "Name": "Lauryn Chenet Williams",
            "Sex": "F",
            "Age": 21,
            "Season": "Summer",
            "Year": 2004,
            "Sport": "Athletics",
            "Medal": "Silver",
        },
        {
            "ID": 130626,
            "Name": "Lauryn Chenet Williams",
            "Sex": "F",
            "Age": 29,
            "Season": "Summer",
            "Year": 2012,
            "Sport": "Athletics",
            "Medal": "Gold",
        },
        {
            "ID": 130626,
            "Name": "Lauryn Chenet Williams",
            "Sex": "F",
            "Age": 31,
            "Season": "Winter",
            "Year": 2014,
            "Sport": "Bobsleigh",
            "Medal": "Silver",
        },
        # Athlète fictif avec le même sport dans les deux saisons
        {
            "ID": 999999,
            "Name": "Athlète Fictif",
            "Sex": "M",
            "Age": 25,
            "Season": "Summer",
            "Year": 2000,
            "Sport": "Swimming",
            "Medal": "Gold",
        },
        {
            "ID": 999999,
            "Name": "Athlète Fictif",
            "Sex": "M",
            "Age": 28,
            "Season": "Winter",
            "Year": 2002,
            "Sport": "Swimming",
            "Medal": "Silver",
        },
    ]
    return pd.DataFrame(data)


def test_nombre_athletes_ete_hiver(donnees_test):
    athletes = trouver_athletes_ete_hiver(donnees_test)

    assert len(athletes) == 5, f"Attendu: 5 athlètes, Obtenu: {len(athletes)}"


def test_identite_athletes_ete_hiver(donnees_test):
    """Teste que la fonction trouve les bons athlètes"""
    athletes = trouver_athletes_ete_hiver(donnees_test)

    # Extraire les IDs des athlètes trouvés
    athlete_ids = [athlete["ID"] for athlete in athletes]

    # Les IDs attendus des 5 athlètes
    expected_ids = [31167, 50859, 102862, 119489, 130626]

    # Vérifier que tous les IDs attendus sont présents
    assert set(athlete_ids) == set(
        expected_ids
    ), "Les IDs attendus ne correspondent pas aux IDs trouvés"


def test_athlete_meme_annee(donnees_test):
    athletes = trouver_athletes_ete_hiver(donnees_test)

    # Trouver les athlètes avec des années communes
    athletes_meme_annee = [a for a in athletes if a["deux_saisons"]]

    # Il devrait y avoir exactement un athlète médaillé aux deux saisons la même année
    assert (
        len(athletes_meme_annee) == 1
    ), f"Attendu: 1 athlète la même année, Obtenu: {len(athletes_meme_annee)}"

    # Vérifier que c'est bien Christa Rothenburger-Luding
    assert (
        athletes_meme_annee[0]["ID"] == 102862
    ), f"L'ID attendu est 102862, Obtenu: {athletes_meme_annee[0]['ID']}"

    # Vérifier que l'année commune est 1988
    assert athletes_meme_annee[0]["deux_saisons"] == [
        1988
    ], "L'année commune attendue est 1988,"
    f"Obtenu: {athletes_meme_annee[0]['deux_saisons']}"


def test_annees_correctes(donnees_test):
    athletes = trouver_athletes_ete_hiver(donnees_test)

    # Vérifier quelques cas spécifiques
    for athlete in athletes:
        if athlete["ID"] == 31167:  # Eddie Eagan
            assert athlete["annees_saison"]["Summer"] == [
                1920
            ], "Années d'été incorrectes pour Eddie Eagan"
            assert athlete["annees_saison"]["Winter"] == [
                1932
            ], "Années d'hiver incorrectes pour Eddie Eagan"

        elif athlete["ID"] == 102862:  # Christa Rothenburger-Luding
            assert set(athlete["annees_saison"]["Summer"]) == {
                1988
            }, "Années d'été incorrectes pour Christa Rothenburger-Luding"
            assert set(athlete["annees_saison"]["Winter"]) == {
                1984,
                1988,
                1992,
            }, "Années d'hiver incorrectes pour Christa Rothenburger-Luding"
