# Ce programme Python donne le nombre de sportifs par édition et par sports.
# Il affiche ensuite trois graphiques avec les 24 sports qui ont compté
# le plus de participants : un premier graphique avec les 8 premiers sports,
# un deuxième avec les 8 sports suivants (du 9e sport au 16e)
# et un dernier avec encore les 8 suivants (donc du 17e sport au 24e).
# ATTENTION : CHANGER LE CHEMIN DU FICHIER SI BESOIN

import pandas
import os
import matplotlib.pyplot as plt

pandas.set_option("display.max_rows", 910)

# Lire le fichier .csv avec la base de données
BDJO = pandas.read_csv(os.path.join("donnees_jeux_olympiques", "athlete_events.csv"))

# Comment évolue le nombre de sportifs par sport au fil des différentes éditions ?

BDJOevo = BDJO
BDJOevo.drop(
    columns=[
        "Sex",
        "Height",
        "Name",
        "Age",
        "Weight",
        "Team",
        "NOC",
        "Games",
        "Season",
        "City",
        "Event",
        "Medal",
    ],
    inplace=True,
)
# Il ne reste plus que les trois colonnes ID, Year, Sport.
BDJOevo.drop_duplicates(keep="first", inplace=True)
# On ne garde qu’une seule donnée par sportif pour un sport et une année donnés.
BDJOevo.drop(
    columns=["ID"],
    inplace=True,
)
# Je supprime la colonne ID une fois que je n’ai gardé le même sportif qu’une fois par
# sport et par édition des Jeux Olympiques.
nbSportifsparSportetAnnee = BDJOevo.groupby(["Sport", "Year"]).size()
# Je compte le nombre de ligne (et donc de sportifs) par sport et par édition.
trinbSportifs = nbSportifsparSportetAnnee.sort_values(ascending=True)
# Je les classe par ordre croissant avant d’afficher le résultat.
print(trinbSportifs)

nbSportifsparSportetAnnee = nbSportifsparSportetAnnee.reset_index(name="Nbre_Sportifs")

plt.figure(figsize=(14, 8))

# Je crée une ligne pour les huit sports qui cumulent
# le plus de participants de 1896 à 2016.
sports_to_plot = (
    nbSportifsparSportetAnnee.groupby("Sport")["Nbre_Sportifs"]
    .sum()
    .sort_values(ascending=False)
    .head(8)
    .index
)
for sport in sports_to_plot:
    sport_data = nbSportifsparSportetAnnee[nbSportifsparSportetAnnee["Sport"] == sport]
    plt.scatter(sport_data["Year"], sport_data["Nbre_Sportifs"], label=sport, alpha=0.6)

# Je personnalise le graphique...
plt.title("Évolution du nombre de sportifs par sport pour les huit premiers sports")
plt.xlabel("Année")
plt.ylabel("Nombre de sportifs")
plt.legend(title="Sport", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()

# ...avant de l’afficher.
plt.show()

# Je crée une ligne pour les huit sports suivants (du 9e au 16e sport) qui cumulent
# le plus de participants de 1896 à 2016.
sports_to_plot2 = (
    nbSportifsparSportetAnnee.groupby("Sport")["Nbre_Sportifs"]
    .sum()
    .sort_values(ascending=False)
    .iloc[8:16]
    .index
)
for sport in sports_to_plot2:
    sport_data = nbSportifsparSportetAnnee[nbSportifsparSportetAnnee["Sport"] == sport]
    plt.scatter(sport_data["Year"], sport_data["Nbre_Sportifs"], label=sport, alpha=0.6)

# Je personnalise le graphique...
plt.title("Évolution du nombre de sportifs par sport pour les 9e au 16e sports")
plt.xlabel("Année")
plt.ylabel("Nombre de sportifs")
plt.legend(title="Sport", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()

# ...avant de l’afficher.
plt.show()

# Je crée une ligne pour les huit sports suivants (du 17e au 24e sport) qui cumulent
# le plus de participants de 1896 à 2016.
sports_to_plot3 = (
    nbSportifsparSportetAnnee.groupby("Sport")["Nbre_Sportifs"]
    .sum()
    .sort_values(ascending=False)
    .iloc[16:24]
    .index
)
for sport in sports_to_plot3:
    sport_data = nbSportifsparSportetAnnee[nbSportifsparSportetAnnee["Sport"] == sport]
    plt.scatter(sport_data["Year"], sport_data["Nbre_Sportifs"], label=sport, alpha=0.6)

# Je personnalise le graphique...
plt.title("Évolution du nombre de sportifs par sport pour les 17e au 24e sports")
plt.xlabel("Année")
plt.ylabel("Nombre de sportifs")
plt.legend(title="Sport", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()

# ...avant de l’afficher.
plt.show()

"""le programme affiche (taille) :
Sport                      Year
Aeronautics                1936       1
Alpinism                   1936       2
                           1932       2
Basque Pelota              1900       2
Roque                      1904       4
Weightlifting              1904       5
Diving                     1904       5
Wrestling                  1896       5
Weightlifting              1896       7
Racquets                   1908       7
Croquet                    1900      10
Skeleton                   1928      10
Art Competitions           1920      11
Fencing                    1904      11
Jeu De Paume               1908      11
Polo                       1908      12
Tug-Of-War                 1900      12
Tennis                     1896      13
Swimming                   1896      13
Weightlifting              1906      13
Motorboating               1908      14
Skeleton                   1948      15
Fencing                    1896      15
Curling                    1924      16
Tug-Of-War                 1912      16
Polo                       1920      17
Cycling                    1904      18
Boxing                     1904      18
Cycling                    1896      19
Polo                       1900      20
Alpinism                   1924      21
Water Polo                 1904      21
Polo                       1936      21
Figure Skating             1908      21
Golf                       1900      22
Archery                    1900      23
Modern Pentathlon          1920      23
Polo                       1924      24
Military Ski Patrol        1924      24
Diving                     1906      24
Cricket                    1900      24
Trampolining               2000      24
Lacrosse                   1908      24
Nordic Combined            1952      25
Modern Pentathlon          1932      25
Tennis                     1900      26
Figure Skating             1920      26
Tennis                     1906      27
Ski Jumping                1924      27
Nordic Combined            1984      28
Gymnastics                 1896      28
Water Polo                 1908      28
Diving                     1932      28
Archery                    1904      29
Weightlifting              1932      29
Figure Skating             1924      29
Tug-Of-War                 1904      30
Archery                    1920      30
Rugby                      1908      30
Biathlon                   1960      30
Nordic Combined            1924      30
Speed Skating              1924      31
                           1932      31
Equestrianism              1932      31
Nordic Combined            1980      31
Rugby                      1920      31
Swimming                   1904      32
Modern Pentathlon          1996      32
Trampolining               2004      32
Modern Pentathlon          1912      32
Nordic Combined            1964      32
Trampolining               2012      32
                           2016      32
                           2008      32
Tug-Of-War                 1906      32
Nordic Combined            1932      33
Rhythmic Gymnastics        1984      33
Nordic Combined            1960      33
Art Competitions           1912      33
Ski Jumping                1932      34
Nordic Combined            1976      34
                           1928      35
Football                   1900      35
Wrestling                  1906      36
Football                   1904      36
Nordic Combined            1956      36
Tennis                     1904      36
Lacrosse                   1904      36
Modern Pentathlon          1928      37
                           1964      37
Ski Jumping                1928      38
Shooting                   1896      38
Modern Pentathlon          1924      38
Rhythmic Gymnastics        1988      39
Nordic Combined            1948      39
Diving                     1908      39
Skeleton                   2002      39
Bobsleigh                  1924      39
Figure Skating             1932      39
Speed Skating              1928      40
Modern Pentathlon          1956      40
Tug-Of-War                 1920      40
Nordic Combined            1972      40
Tug-Of-War                 1908      40
Hockey                     1932      40
Nordic Combined            1968      41
Water Polo                 1932      41
Bobsleigh                  1932      41
Shooting                   1932      41
Rhythmic Gymnastics        1992      42
Skeleton                   2006      42
Wrestling                  1904      42
Modern Pentathlon          1936      42
Boxing                     1908      42
Swimming                   1906      43
Modern Pentathlon          1980      43
Rowing                     1904      44
Nordic Combined            1988      44
Ski Jumping                1952      44
Football                   1906      45
Modern Pentathlon          1948      45
Water Polo                 1912      45
Cycling                    1906      45
Ski Jumping                1960      45
Nordic Combined            1992      46
Gymnastics                 1932      46
Skeleton                   2014      46
Synchronized Swimming      1988      46
Modern Pentathlon          1976      47
Rugby                      1900      47
Skeleton                   2010      47
Modern Pentathlon          1968      48
Ice Hockey                 1932      48
Ski Jumping                1936      48
Modern Pentathlon          2000      48
Ski Jumping                1948      49
Tennis                     1908      50
Synchronized Swimming      1984      50
Ski Jumping                1956      51
Nordic Combined            1936      51
Modern Pentathlon          1952      51
Biathlon                   1964      51
Hockey                     1920      51
Figure Skating             1928      51
Nordic Combined            2010      52
Speed Skating              1936      52
Modern Pentathlon          1984      52
Synchronized Swimming      1992      53
Water Polo                 1900      53
Diving                     1920      53
Weightlifting              1920      53
Nordic Combined            1994      53
                           1998      53
Sailing                    1932      54
Nordic Combined            2014      54
Rugby                      1924      54
Nordic Combined            2002      54
Ski Jumping                1980      55
                           1964      57
Diving                     1912      57
Archery                    1908      57
Cross Country Skiing       1932      58
Equestrianism              1900      58
Nordic Combined            2006      59
Modern Pentathlon          1972      59
Cross Country Skiing       1924      59
Figure Skating             1956      59
Diving                     1956      60
Modern Pentathlon          1960      60
Ice Hockey                 1920      60
Diving                     1928      61
Ski Jumping                1976      62
                           1972      62
Biathlon                   1972      62
Fencing                    1906      62
Equestrianism              1912      62
Ski Jumping                1992      63
Athletics                  1896      63
Figure Skating             1952      63
Diving                     1948      63
Figure Skating             1948      64
Archery                    1976      64
Modern Pentathlon          2004      64
Sailing                    1908      64
Modern Pentathlon          1988      65
Ski Jumping                1984      65
                           1988      65
Sailing                    1924      65
Cycling                    1932      66
Modern Pentathlon          1992      66
Ski Jumping                1968      66
Speed Skating              1952      67
Figure Skating             1972      67
Archery                    1980      67
Diving                     1980      67
Speed Skating              1948      68
Equestrianism              1980      68
Shooting                   1906      68
Ski Jumping                1998      68
                           1994      68
Hockey                     1908      68
Ski Jumping                2010      68
Luge                       1964      68
Diving                     1936      69
Bobsleigh                  1952      70
Diving                     1924      71
Freestyle Skiing           1992      71
Figure Skating             1960      71
Bobsleigh                  1948      71
Football                   1908      72
Modern Pentathlon          2008      72
Judo                       1964      72
Modern Pentathlon          2012      72
                           2016      72
Cycling                    1900      72
Synchronized Swimming      1996      72
Gymnastics                 1924      72
Biathlon                   1968      72
Shooting                   1900      72
Ski Jumping                2002      73
Cross Country Skiing       1928      74
Biathlon                   1976      74
Diving                     1960      75
Tennis                     1920      75
Diving                     1952      76
Swimming                   1900      76
Biathlon                   1980      76
Golf                       1904      77
Bobsleigh                  1980      78
                           1972      79
Ski Jumping                2006      79
Wrestling                  1932      79
Diving                     1976      80
                           1984      80
                           1964      80
Luge                       1980      80
Tennis                     1912      80
Curling                    1998      80
Weightlifting              1936      80
Rowing                     1908      81
Luge                       1984      81
Diving                     1968      81
Bobsleigh                  1964      81
Ice Hockey                 1924      82
Speed Skating              1956      83
Luge                       1972      83
Rhythmic Gymnastics        2004      84
Figure Skating             1980      84
Rhythmic Gymnastics        2000      84
Figure Skating             1936      84
Beach Volleyball           1996      84
Luge                       1968      85
Boxing                     1932      85
Short Track Speed Skating  1992      86
Curling                    2014      87
Short Track Speed Skating  1994      87
Figure Skating             1964      88
Luge                       1992      89
Equestrianism              1920      89
Diving                     1988      89
Rhythmic Gymnastics        1996      90
Bobsleigh                  1968      90
Luge                       1988      90
Biathlon                   1988      90
Diving                     1972      91
Curling                    2006      91
Luge                       1994      92
Bobsleigh                  1976      92
Curling                    2010      93
Luge                       1998      93
                           1976      94
Weightlifting              1928      94
Short Track Speed Skating  1998      94
Rhythmic Gymnastics        2012      95
Biathlon                   1984      95
Bobsleigh                  1936      95
Archery                    1972      95
Rhythmic Gymnastics        2008      95
                           2016      96
Water Polo                 1956      96
Beach Volleyball           2000      96
Curling                    2002      96
Beach Volleyball           2008      96
Figure Skating             1968      96
Beach Volleyball           2012      96
                           2016      96
Ski Jumping                2014      96
Beach Volleyball           2004      96
Sailing                    1900      96
Freestyle Skiing           1994      97
Cycling                    1908      97
Equestrianism              1924      97
Triathlon                  2004      99
Rowing                     1900      99
Diving                     1992     100
Triathlon                  2000     100
Swimming                   1908     100
Bobsleigh                  1956     101
Synchronized Swimming      2000     101
                           2012     101
                           2004     101
Sailing                    1920     101
Water Polo                 1924     101
                           1920     101
Taekwondo                  2000     102
Synchronized Swimming      2008     102
                           2016     102
Cycling                    1920     103
Equestrianism              1948     103
Speed Skating              1960     103
Alpine Skiing              1936     103
Gymnastics                 1906     104
Weightlifting              1956     105
Handball                   1936     105
Freestyle Skiing           2002     105
Figure Skating             1976     105
Cross Country Skiing       1948     106
Short Track Speed Skating  2014     106
                           2006     106
Weightlifting              1924     107
Luge                       2010     107
                           2014     108
Fencing                    1932     108
Luge                       2006     108
Archery                    1984     109
Cross Country Skiing       1936     109
Short Track Speed Skating  2010     109
Sailing                    1912     109
Canoeing                   1948     110
Freestyle Skiing           1998     110
Luge                       2002     110
Triathlon                  2012     110
                           2016     110
                           2008     110
Bobsleigh                  1984     111
Speed Skating              1976     111
Short Track Speed Skating  2002     111
Cross Country Skiing       1960     112
Water Polo                 1928     112
Canoeing                   1956     113
Equestrianism              1928     113
Figure Skating             1984     114
Wrestling                  1908     115
Athletics                  1904     116
Equestrianism              1964     116
Bobsleigh                  1928     116
Swimming                   1920     116
Boxing                     1920     116
Freestyle Skiing           2006     116
Snowboarding               2002     118
Speed Skating              1972     118
Softball                   2004     118
Athletics                  1900     119
Canoeing                   1936     119
Swimming                   1912     120
Softball                   2008     120
                           1996     120
Weightlifting              1948     120
Golf                       2016     120
Softball                   2000     120
Gymnastics                 1904     121
Diving                     1996     122
Cycling                    1912     123
Taekwondo                  2004     124
Ice Hockey                 1928     124
Tennis                     1924     124
Equestrianism              1968     125
Snowboarding               1998     125
Taekwondo                  2016     126
                           2008     126
Sailing                    1928     127
Gymnastics                 1980     127
Equestrianism              1936     127
Speed Skating              1980     128
Gymnastics                 1956     128
Archery                    1996     128
Taekwondo                  2012     128
Swimming                   1932     128
Archery                    2000     128
                           2004     128
                           2016     128
                           2012     128
                           2008     128
Figure Skating             1994     129
Tennis                     1988     129
Table Tennis               1988     129
Speed Skating              1968     129
Figure Skating             1988     129
Diving                     2004     129
Cross Country Skiing       1980     130
Fencing                    1908     131
Water Polo                 1976     131
                           1980     132
Alpine Skiing              1960     133
Figure Skating             1992     133
Speed Skating              1964     134
Equestrianism              1952     134
Gymnastics                 1900     135
Bobsleigh                  1988     135
Equestrianism              1976     135
Judo                       1976     136
Gymnastics                 1984     136
Archery                    1992     136
Rowing                     1920     136
Diving                     2012     136
                           2016     136
Hockey                     1928     137
Water Polo                 1964     137
Cross Country Skiing       1952     138
Ice Hockey                 1948     139
Speed Skating              1984     139
Cycling                    1924     139
Diving                     2008     140
Shooting                   1936     141
Speed Skating              1988     141
Weightlifting              1952     142
Water Polo                 1936     142
Figure Skating             2002     143
Alpine Skiing              1972     143
Football                   1956     143
Boxing                     1928     144
Gymnastics                 1928     144
Canoeing                   1964     145
Figure Skating             1998     145
                           2010     146
Archery                    1988     146
Ice Hockey                 1952     147
Figure Skating             2006     147
Cross Country Skiing       1968     147
Judo                       1972     148
Figure Skating             2014     149
Weightlifting              1964     149
Cycling                    1928     149
Fencing                    1920     149
Water Polo                 1960     150
Bobsleigh                  2006     150
Cross Country Skiing       1956     150
Speed Skating              1994     150
Cross Country Skiing       1964     151
Water Polo                 1992     152
Ice Hockey                 1960     152
Wrestling                  1920     152
Rowing                     1932     152
Cross Country Skiing       1972     152
Water Polo                 1996     153
                           1984     153
Sailing                    1956     154
Speed Skating              1992     154
Bobsleigh                  1994     155
Sailing                    1980     156
Water Polo                 1988     156
Shooting                   1956     156
Water Polo                 1948     156
Bobsleigh                  1998     156
Diving                     2000     157
Hockey                     1952     157
Equestrianism              1984     157
                           1956     158
Bobsleigh                  1992     159
Table Tennis               1992     159
Bobsleigh                  2010     159
Canoeing                   1952     159
Equestrianism              1960     159
Baseball                   1992     160
                           1996     160
Weightlifting              1968     160
Cycling                    1956     161
Boxing                     1956     161
Water Polo                 1968     162
Football                   1912     163
Cross Country Skiing       1976     164
Fencing                    1956     165
Speed Skating              2002     166
Alpine Skiing              1952     166
Table Tennis               1996     166
Wrestling                  1928     166
Rowing                     1906     167
Alpine Skiing              1948     167
Hockey                     1936     167
Ice Hockey                 1956     169
Basketball                 1956     169
Tennis                     2008     169
Swimming                   1924     169
Tennis                     2004     170
Wrestling                  1912     170
Table Tennis               2000     171
Badminton                  2000     171
Speed Skating              1998     171
Table Tennis               2008     171
Hockey                     1976     172
Freestyle Skiing           2010     172
Table Tennis               2016     172
Badminton                  2004     172
Table Tennis               2004     172
Bobsleigh                  2014     172
Badminton                  2016     172
Weightlifting              1980     172
Badminton                  2012     172
Sailing                    1936     172
Weightlifting              1960     172
Canoeing                   1960     173
Weightlifting              1976     173
Hockey                     1956     173
Badminton                  2008     173
Wrestling                  1956     173
Ice Hockey                 1936     173
Alpine Skiing              1980     174
                           1964     174
Speed Skating              2006     174
Table Tennis               2012     174
Gymnastics                 1936     175
Cycling                    1936     175
Water Polo                 1972     176
Tennis                     1996     176
Gymnastics                 1976     176
Badminton                  1992     177
Speed Skating              2014     177
                           2010     177
Tennis                     1992     177
Equestrianism              1972     179
Volleyball                 1964     179
Cross Country Skiing       1984     179
Gymnastics                 1988     179
Boxing                     1936     179
Canoeing                   1980     180
Boxing                     1924     181
Rowing                     1924     181
Alpine Skiing              1976     181
Tennis                     2000     182
Equestrianism              1988     182
Swimming                   1928     182
Judo                       1980     182
Alpine Skiing              1956     183
Biathlon                   1998     183
Rowing                     1912     184
Canoeing                   1968     184
Tennis                     2012     184
Fencing                    1912     185
Gymnastics                 1992     185
Snowboarding               2010     185
Weightlifting              1984     186
Sailing                    1948     186
Snowboarding               2006     187
Hockey                     1948     187
                           1980     187
Fencing                    1980     187
Shooting                   1948     188
Weightlifting              1972     188
Cycling                    1948     188
Art Competitions           1924     189
Basketball                 1964     189
Biathlon                   2002     190
Football                   1920     190
Basketball                 1972     190
Baseball                   2008     191
                           2004     191
Basketball                 1968     191
Water Polo                 1952     191
Alpine Skiing              1968     191
Basketball                 1960     192
Badminton                  1996     192
Baseball                   2000     192
Biathlon                   1994     193
Equestrianism              2008     193
Gymnastics                 2000     194
                           2012     195
Bobsleigh                  2002     195
Equestrianism              2000     195
Canoeing                   1984     195
Gymnastics                 2016     196
Biathlon                   1992     196
Gymnastics                 2008     196
                           2004     196
Tennis                     2016     196
Cross Country Skiing       1994     197
                           1988     198
Equestrianism              2012     199
Basketball                 1936     199
Wrestling                  1936     200
Equestrianism              2016     200
Football                   1936     201
                           1976     202
Equestrianism              2004     203
Volleyball                 1980     204
Biathlon                   2014     204
                           2006     204
                           2010     204
Boxing                     1948     205
Volleyball                 1968     206
Ice Hockey                 1972     208
Volleyball                 1984     208
Gymnastics                 1948     211
Judo                       1984     212
Gymnastics                 1964     213
Basketball                 1984     213
                           1976     213
Football                   1964     214
Cycling                    1952     215
Basketball                 1980     215
Shooting                   1908     215
Equestrianism              1992     215
Gymnastics                 1996     216
Volleyball                 1976     216
Ice Hockey                 1976     217
Fencing                    2000     217
Football                   1948     218
Gymnastics                 1968     218
Shooting                   1952     218
Wrestling                  1948     219
Football                   1928     219
Equestrianism              1996     219
Fencing                    2004     222
Cross Country Skiing       1992     223
Fencing                    1996     224
Alpine Skiing              1984     225
Sailing                    1964     225
Weightlifting              1988     226
Hockey                     1964     226
Sailing                    1952     227
Cross Country Skiing       1998     227
Wrestling                  1924     229
Cycling                    1980     230
Gymnastics                 1972     231
Water Polo                 2000     231
Volleyball                 1972     231
                           1992     231
Athletics                  1906     233
Fencing                    2008     234
Swimming                   1956     235
Football                   1960     235
Shooting                   1920     236
Hockey                     1960     236
Basketball                 1992     236
                           1988     236
Snowboarding               2014     237
Volleyball                 1988     239
Ice Hockey                 1984     239
Shooting                   1980     239
Ice Hockey                 1980     239
Fencing                    1924     240
Rowing                     1956     242
Weightlifting              1996     243
Judo                       1988     243
Handball                   1972     243
                           1976     243
Weightlifting              1992     244
Rowing                     1928     244
Fencing                    2012     244
Wrestling                  1952     244
Fencing                    2016     245
Canoeing                   1976     245
Weightlifting              2000     246
Football                   1984     246
Swimming                   1936     248
Handball                   1980     248
Gymnastics                 1920     249
Swimming                   1948     249
Weightlifting              2004     249
Alpine Skiing              1998     249
Boxing                     1952     249
Gymnastics                 1912     249
Ice Hockey                 1968     250
Alpine Skiing              1994     250
Sailing                    1968     251
Weightlifting              2012     252
                           2008     253
Hockey                     1968     253
Gymnastics                 1960     254
Weightlifting              2016     255
Water Polo                 2004     255
Football                   1980     256
Water Polo                 2008     256
Sailing                    1976     257
Water Polo                 2012     257
Shooting                   1924     258
Water Polo                 2016     258
Handball                   1984     259
Fencing                    1964     259
                           1928     259
Cross Country Skiing       2002     260
Fencing                    1900     260
Freestyle Skiing           2014     262
Shooting                   1964     262
Fencing                    1984     262
Hockey                     1972     263
Ice Hockey                 1988     265
Boxing                     1976     266
Wrestling                  1980     266
Ice Hockey                 1992     267
Wrestling                  1984     267
Ice Hockey                 1994     268
Boxing                     1964     269
Football                   1972     269
Ice Hockey                 1964     270
Football                   1988     270
Boxing                     1980     271
Football                   1992     272
Alpine Skiing              1988     272
Football                   1968     273
Volleyball                 1996     275
Fencing                    1968     275
Canoeing                   1988     275
Wrestling                  1964     275
Alpine Skiing              2002     278
Volleyball                 2000     279
Football                   1924     279
Boxing                     2004     280
                           1960     281
Basketball                 2016     281
Handball                   1988     281
Fencing                    1976     281
Volleyball                 2008     283
                           2016     283
                           2004     283
Boxing                     2012     283
                           2008     283
                           2016     283
Basketball                 1996     284
Shooting                   1912     284
Basketball                 2000     286
Hockey                     1984     286
Fencing                    1952     286
Alpine Skiing              2006     287
Basketball                 2004     287
                           1948     287
                           2008     287
                           2012     287
Volleyball                 2012     287
Sailing                    1960     290
Cross Country Skiing       2010     292
Handball                   1992     292
Basketball                 1952     294
Fencing                    1948     294
Football                   1952     294
Cycling                    1976     295
Wrestling                  1968     297
Cycling                    1960     297
Cross Country Skiing       2014     298
Rugby Sevens               2016     299
Fencing                    1972     299
Handball                   1996     300
Sailing                    1984     300
Cycling                    1964     303
Fencing                    1992     305
Cross Country Skiing       2006     307
Boxing                     2000     307
                           1968     307
Alpine Skiing              2010     309
Rowing                     1948     310
Fencing                    1936     311
Shooting                   1960     313
Wrestling                  2000     314
Hockey                     1992     314
                           1988     314
Alpine Skiing              2014     314
Rowing                     1936     314
Fencing                    1988     317
Swimming                   1952     319
Gymnastics                 1952     319
Hockey                     1996     320
Alpine Skiing              1992     321
Handball                   2000     323
Sailing                    1972     323
Wrestling                  1960     324
Gymnastics                 1908     325
Handball                   2004     328
Canoeing                   2004     328
Cycling                    1968     329
Wrestling                  1976     330
Canoeing                   1972     330
                           2008     330
                           2000     330
                           2016     330
Art Competitions           1948     330
Canoeing                   2012     332
Swimming                   1980     333
Boxing                     1992     336
Wrestling                  2012     339
                           2004     342
Handball                   2008     343
Wrestling                  2008     343
Fencing                    1960     344
Shooting                   1976     344
Wrestling                  2016     346
Handball                   2012     347
Hockey                     2000     350
Shooting                   1968     351
Hockey                     2004     352
Handball                   2016     353
Rowing                     1968     353
Boxing                     1984     354
                           1972     354
                           1996     355
Cycling                    1972     359
                           1984     359
Art Competitions           1928     370
Wrestling                  1992     370
Rowing                     1964     370
Sailing                    1988     375
                           2012     379
                           2016     380
Swimming                   1960     380
Judo                       2004     384
                           2012     384
Athletics                  1932     386
Judo                       2008     386
Hockey                     2008     387
                           2012     387
Judo                       1996     387
Wrestling                  1972     388
Football                   1996     388
Judo                       2016     389
Hockey                     2016     390
Shooting                   2004     390
                           2008     390
                           2012     390
                           2016     390
Football                   2000     391
Shooting                   1988     396
                           1972     397
Judo                       2000     398
Sailing                    2008     400
                           2004     400
Wrestling                  1996     401
Sailing                    2000     402
Rowing                     1952     404
Swimming                   1964     405
Shooting                   1992     407
                           2000     408
Rowing                     1960     410
Shooting                   1996     419
Ice Hockey                 2010     420
Cycling                    1988     422
Football                   2004     425
Ice Hockey                 1998     426
Wrestling                  1988     429
Athletics                  1908     431
Boxing                     1988     432
Judo                       1992     433
Canoeing                   1992     440
Rowing                     1972     440
Sailing                    1992     441
Ice Hockey                 2006     442
                           2014     443
Rowing                     1984     447
Cycling                    1992     451
Canoeing                   1996     451
Sailing                    1996     458
Shooting                   1984     460
Cycling                    2000     462
                           2004     464
Football                   2012     467
Swimming                   1968     468
Ice Hockey                 2002     468
Football                   2008     469
Rowing                     1980     470
Swimming                   1976     471
Football                   2016     473
Cycling                    1996     477
Swimming                   1984     494
Cycling                    2012     501
                           2008     508
Athletics                  1920     509
Cycling                    2016     513
Art Competitions           1936     527
Swimming                   1972     532
Athletics                  1912     534
Rowing                     2016     546
                           2000     547
                           2012     549
                           2008     555
                           2004     557
Art Competitions           1932     588
Rowing                     1976     593
                           1988     593
                           1996     608
                           1992     627
Swimming                   1988     633
                           1992     641
Athletics                  1924     659
                           1928     706
                           1956     720
                           1948     745
Swimming                   1996     762
Athletics                  1936     776
Swimming                   2012     931
                           2004     937
                           2016     942
                           2000     954
Athletics                  1980     960
                           1952     963
                           1976    1006
                           1960    1016
                           1964    1018
Swimming                   2008    1022
Athletics                  1968    1029
                           1984    1280
                           1972    1330
                           1988    1618
                           1992    1726
                           2004    1995
                           2008    2056
                           1996    2057
                           2012    2079
                           2000    2137
                           2016    2269"""
