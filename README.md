****************************************************
* Projet d'analyse des données des jeux olympiques *
****************************************************

Description
-----------

Ce projet vise à analyser les données des Jeux Olympiques modernes à l'aide de
différentes méthodes de traitement de données.

Il inclut l'analyse des performances des athlètes, la classification des épreuves
sportives en fonction des caractéristiques physiques des athlètes, et la comparaison
des performances entre différentes nations au cours des différentes éditions des Jeux.

Le code est divisé en plusieurs modules, chacun ayant une fonction spécifique,
allant de la gestion des données brutes à l'application d'algorithmes de classification.
Le projet utilise des bibliothèques comme Pandas, NumPy, Scikit-learn, et Tkinter pour
l'analyse et l'interface graphique.


Pré-requis
---------

Avant d'exécuter ce projet, assurez-vous d'avoir installé les packages suivants :

    Python 3.x
    Pandas
    NumPy
    Scikit-learn
    Matplotlib (pour les visualisations)
    Tkinter (pour l'interface graphique)
    Openpxyl


Installation
------------

Enregistrer le dossier code_traitement_donnees dans votre ordinateur
Ouvrir un environnement de développement tel que Visual Studio Code
Dans File, sélectionner Open Folder et choisir le dossier code_traitement_donnees
Lancer le fichier main.py du dossier /src
Ce fichier "main" est l'entrée principale qui fait appel à l'ensemble des modules du projet de traitement de données
Une interface graphique s'affichera avec un menu déroulant


Utilisation de l'interface graphique
------------------------------------

# Réponses aux questions du projet de traitement de données
Sélectionner dans le menu déroulant les questions de 1 à 9
N.B. : la question 6 regroupe à elle seule 3 questions (cf. rapport : questions 6a, 6b et 6c)
Lorsque vous sélectionnez les questions 1 à 4, une interface Tkinter s'affiche.
La question 3 peut prendre un certain temps avant d'afficher le résultat.
Pour la question 5, il faut remplir les champs avant de lire la réponse de la question dans la console.
Les questions de 6 à 9 ne nécessitent pas de remplir de champs sur la console, la réponse à la question s'affiche dans la console.
La question 7 affiche en plus d'un tableau dans la console trois graphiques successifs.
Toutes les réponses des questions 1 à 9 sont enregistrées dans les sous-dossiers des questions associées du dossier /output.

# Réponses de la problématique
Pour obtenir les réponses de la problématique, il faut sélectionner 3 éléments :
1 - Test_kmeans : qui permet de comparer le kmeans que nous implémentons et celui de Scikit-learn
2 - Critere_coude : qui lance un module implémenté par nous-mêmes pour choisir le nombre de classes avec le critère du coude
3 - Classification : qui renvoie les solutions de notre classification répondant à notre problématique
Lorsque vous sélectionnez une de ces champs de la liste déroulante, une interface Tkinter s'affiche
Toutes les réponses de la problématique sont enregistrées dans le dossier /problematique


Structure du projet
-------------------

Le projet est organisé en plusieurs répertoires pour une meilleure gestion et modularité du code :
.
├── __pycache__/
│   ├── algo_kmeans.cpython-312.pyc
│   ├── arbo.cpython-312.pyc
│   ├── arboresence.cpython-312.pyc
│   ├── distance_euclidienne.cpython-312.pyc
│   └── renormalisation.cpython-312.pyc
├── donnees/
│   ├── athlete_events.csv
│   ├── noc_regions.csv
│   ├── classification/
│   │   ├── typologie_clusters.png
│   │   └── typologie_clusters.txt
│   └── problematique/
│       └── typologie_clusters.txt
├── output/
│   ├── analyse_donnees/
│   ├── problematique/
│   ├── question_1/
│   ├── question_2/
│   ├── question_3/
│   ├── question_4/
│   ├── question_5/
│   ├── question_6/
│   ├── question_7/
│   ├── question_8/
│   └── question_9/
├── programmes/
│   ├── __init__.py
│   ├── __pycache__/
│   │   ├── __init__.cpython-312.pyc
│   │   └── decouverte_base.cpython-312.pyc
│   ├── decouverte_base.py
│   ├── classification/
│   │   ├── __init__.py
│   │   ├── algo_kmeans.py
│   │   ├── critere_coude.py
│   │   ├── distance_euclidienne.py
│   │   ├── donnees_classification.py
│   │   ├── initialisation_kmean.py
│   │   ├── main.py
│   │   ├── reduction_dimension.py
│   │   ├── renormalisation.py
│   │   ├── test_kmeans.py
│   │   └── __pycache__/
│   │       ├── (fichiers .pyc correspondants)
│   └── questions/
│       ├── __init__.py
│       ├── __pycache__/
│       ├── questions_basepython/
│       │   ├── __init__.py
│       │   ├── question1_basepython.py
│       │   ├── question2_basepython.py
│       │   ├── question3_basepython.py
│       │   ├── question6_basepython.py
│       │   ├── question9_basepython.py
│       │   └── __pycache__/
│       │       ├── (fichiers .pyc correspondants)
│       └── questions_pandapython/
│           ├── __init__.py
│           ├── question1_pandapython.py
│           ├── question2_pandapython.py
│           ├── question3_pandapython.py
│           ├── question4_pandapython.py
│           ├── question5_pandapython.py
│           ├── question6_pandapython.py
│           ├── question7_pandapython.py
│           ├── question8_pandapython.py
│           ├── question9_pandapython.py
│           └── __pycache__/
│               ├── (fichiers .pyc correspondants)
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── __pycache__/
│   │   ├── __init__.cpython-312.pyc
│   │   ├── main.cpython-312.pyc
│   │   └── histograme_question2.cpython-312.pyc
│   ├── interface_graphique/
│   │   ├── __init__.py
│   │   ├── histograme_question2.py
│   │   ├── interface_question1.py
│   │   ├── interface_question2.py
│   │   ├── interface_question3.py
│   │   ├── interface_question4.py
│   │   ├── __pycache__/
│   │   │   ├── (fichiers .pyc correspondants)
│   │   └── resultats/
│   │       └── output_histo.jpg
│   └── tests/
│       ├── compare_temps_execution_question1.py
│       ├── compare_temps_execution_question2.py
│       ├── test_question_1.py
│       ├── test_question_3.py
│       ├── test_question_5.py
│       ├── tests_execution.py
│       └── __pycache__/
│           ├── (fichiers .pyc correspondants)


Auteurs
-------

Teodora
Gabriel
Tual
Khalid
