# Ce programme Python trie les sports selon le sexe par ordre croissant du poids et
# de la taille des participants aux Jeux Olympiques.
# ATTENTION : CHANGER LE CHEMIN DU FICHIER SI BESOIN

import pandas
import os
pandas.set_option('display.max_rows', 120)

# Lire le fichier .csv avec la base de données (CHEMIN DU FICHIER)
BDJO = pandas.read_csv(os.path.join("donnees_jeux_olympiques", "athlete_events.csv"))

# Comment la taille des sportifs varient-ils selon les sports et le sexe ?

BDJOtaille = BDJO.dropna(subset=["Height"])
BDJOtaille.drop(columns=[
    "Name", "Age", "Weight", "Team", "NOC", "Games", "Season", "City", "Event", "Medal"
    ], inplace=True)
# Il ne reste plus que les cinq colonnes ID, Sex, Height, Year, Sport.
BDJOtaille.drop_duplicates(keep='first', inplace=True)
# On ne garde qu’une seule donnée par sportif pour un sport et une année donnés.
BDJOtaille.drop(columns=["ID", "Year"], inplace=True)
# Suppression de deux dernières colonnes inutiles une fois que
# l’on a conservé toutes les données et que les données souhaitées.
tailleGB = BDJOtaille.groupby(by=["Sport", "Sex"]).mean("Height")
tritaille = tailleGB.sort_values(by="Height", ascending=True)
print(tritaille)

# Comment le poids des sportifs varient-ils selon les sports et le sexe ?

BDJOpoids = BDJO.dropna(subset=["Weight"])
BDJOpoids.drop(columns=[
    "Name", "Age", "Height", "Team", "NOC", "Games", "Season", "City", "Event", "Medal"
    ], inplace=True)
# Il ne reste plus que les cinq colonnes ID, Sex, Weight, Year, Sport.
BDJOpoids.drop_duplicates(keep='first', inplace=True)
# On ne garde qu’une seule donnée par sportif pour un sport et une année donnés.
BDJOpoids.drop(columns=["ID", "Year"], inplace=True)
# Suppression de deux dernières colonnes inutiles une fois que
# l’on a conservé toutes les données et que les données souhaitées.
poidsGB = BDJOpoids.groupby(by=["Sport", "Sex"]).mean("Weight")
tripoids = poidsGB.sort_values(by="Weight", ascending=True)
print(tripoids)

"""le programme affiche (taille) :
Gymnastics                F    155.992259
Art Competitions          F    160.000000
Weightlifting             F    160.467391
Figure Skating            F    160.636476
Diving                    F    161.278447
Trampolining              F    161.733333
Wrestling                 F    163.865132
Short Track Speed Skating F    164.430341
Ski Jumping               F    164.600000
Freestyle Skiing          F    164.753488
Shooting                  F    165.025328
Table Tennis              F    165.215278
Hockey                    F    166.125267
Snowboarding              F    166.225806
Judo                      F    166.267000
Biathlon                  F    166.600000
Cross Country Skiing      F    166.604128
Triathlon                 F    166.996183
Archery                   F    167.039539
Alpine Skiing             F    167.120000
Speed Skating             F    167.368990
Curling                   F    167.520362
Rugby Sevens              F    167.636986
Gymnastics                M    167.643489
Football                  F    167.676142
Equestrianism             F    167.754148
Cycling                   F    167.847953
Rhythmic Gymnastics       F    167.870253
Skeleton                  F    167.923077
Ice Hockey                F    168.209549
Badminton                 F    168.332731
Synchronized Swimming     F    168.395415
Golf                      F    168.733333
Boxing                    F    168.800000
Fencing                   F    168.815119
Luge                      F    168.991150
Weightlifting             M    169.139260
Canoeing                  F    169.323858
Softball                  F    169.395089
Athletics                 F    169.476290
Sailing                   F    169.510808
Modern Pentathlon         F    170.073171
Taekwondo                 F    170.811644
Swimming                  F    171.088980
Diving                    M    171.300000
Trampolining              M    171.368421
Tennis                    F    172.155172
Wrestling                 M    172.804702
Boxing                    M    172.888199
Bobsleigh                 F    173.181818
Lacrosse                  M    174.000000
Handball                  F    174.840278
Art Competitions          M    175.166667
Polo                      M    175.500000
Water Polo                F    175.563525
Short Track Speed Skating M    175.637931
Shooting                  M    175.954728
Racquets                  M    176.000000
Figure Skating            M    176.006435
Nordic Combined           M    176.084672
Ski Jumping               M    176.084995
Rugby                     M    176.096774
Freestyle Skiing          M    176.479675
Equestrianism             M    176.535380
Rowing                    F    176.719506
Hockey                    M    176.852577
Table Tennis              M    177.155200
Judo                      M    177.317622
Football                  M    177.480339
Cross Country Skiing      M    177.502452
Cycling                   M    177.818681
Alpine Skiing             M    177.842252
Archery                   M    178.202020
Snowboarding              M    178.411273
Biathlon                  M    178.494828
Jeu De Paume              M    178.500000
Beach Volleyball          F    178.866667
Speed Skating             M    179.186084
Golf                      M    179.191176
Modern Pentathlon         M    179.309013
Badminton                 M    179.405493
Luge                      M    179.414352
Volleyball                F    179.494983
Athletics                 M    180.096915
Sailing                   M    180.164776
Triathlon                 M    180.195489
Fencing                   M    180.270987
Curling                   M    180.709251
Ice Hockey                M    180.991444
Motorboating              M    181.000000
Skeleton                  M    181.072727
Canoeing                  M    181.083663
Bobsleigh                 M    182.060858
Taekwondo                 M    182.418301
Basketball                F    182.454836
Tug-Of-War                M    182.480000
Baseball                  M    182.599291
Rugby Sevens              M    182.834437
Swimming                  M    184.008377
Tennis                    M    184.673854
Water Polo                M    186.801739
Rowing                    M    186.959108
Handball                  M    188.778373
Volleyball                M    193.265660
Beach Volleyball          M    193.290909
Basketball                M    194.872624

et poids :
Gymnastics                F    47.705338
Rhythmic Gymnastics       F    48.760976
Figure Skating            F    49.883941
Ski Jumping               F    52.615385
Trampolining              F    52.893333
Diving                    F    53.651226
Triathlon                 F    54.724138
Synchronized Swimming     F    55.795918
Short Track Speed Skating F    56.925697
Biathlon                  F    57.371151
Cross Country Skiing      F    57.552980
Table Tennis              F    58.238754
Modern Pentathlon         F    58.310976
Freestyle Skiing          F    58.329812
Equestrianism             F    58.523520
Cycling                   F    59.345064
Snowboarding              F    60.333333
Hockey                    F    60.530935
Wrestling                 F    60.554455
Fencing                   F    60.574770
Athletics                 F    60.591120
Football                  F    60.925813
Skeleton                  F    61.000000
Taekwondo                 F    61.136824
Swimming                  F    61.257097
Shooting                  F    61.284588
Badminton                 F    61.477778
Archery                   F    61.758562
Boxing                    F    61.836066
Speed Skating             F    61.965854
Tennis                    F    62.020505
Alpine Skiing             F    62.384682
Sailing                   F    62.777268
Curling                   F    62.888350
Gymnastics                M    63.358355
Golf                      F    63.436364
Canoeing                  F    64.495927
Boxing                    M    65.305153
Ice Hockey                F    65.712865
Trampolining              M    65.837838
Ski Jumping               M    65.842572
Rugby Sevens              F    66.628378
Diving                    M    66.808579
Luge                      F    66.825959
Judo                      F    67.067164
Softball                  F    67.471655
Nordic Combined           M    67.600000
Weightlifting             F    67.724622
Beach Volleyball          F    68.350943
Triathlon                 M    68.803774
Handball                  F    68.876851
Volleyball                F    69.333779
Figure Skating            M    69.476257
Rowing                    F    70.030123
Water Polo                F    70.180328
Equestrianism             M    70.826761
Short Track Speed Skating M    71.442529
Cross Country Skiing      M    71.686932
Table Tennis              M    71.707200
Cycling                   M    72.009934
Modern Pentathlon         M    72.315946
Biathlon                  M    72.432093
Bobsleigh                 F    72.804196
Football                  M    73.086644
Hockey                    M    73.343761
Basketball                F    73.685170
Badminton                 M    74.068966
Athletics                 M    74.463427
Taekwondo                 M    74.653595
Freestyle Skiing          M    74.716356
Fencing                   M    75.513460
Wrestling                 M    76.249481
Speed Skating             M    76.404663
Archery                   M    76.620846
Snowboarding              M    76.665962
Lacrosse                  M    76.714286
Motorboating              M    77.000000
Art Competitions          M    77.187500
Rugby                     M    77.533333
Swimming                  M    77.806805
Shooting                  M    78.003684
Alpine Skiing             M    78.465845
Tennis                    M    78.749658
Sailing                   M    78.857357
Golf                      M    79.245283
Canoeing                  M    79.537161
Weightlifting             M    80.230654
Luge                      M    80.879210
Curling                   M    81.465686
Skeleton                  M    82.018349
Judo                      M    83.228601
Rowing                    M    83.770322
Ice Hockey                M    83.775593
Baseball                  M    85.707792
Volleyball                M    86.925926
Water Polo                M    87.706172
Handball                  M    89.387914
Beach Volleyball          M    89.512821
Bobsleigh                 M    90.264045
Rugby Sevens              M    91.006623
Basketball                M    91.683529
Tug-Of-War                M    95.615385"""
