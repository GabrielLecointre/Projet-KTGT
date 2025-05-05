import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Chargement des données
# -----------------------------
df = pd.read_csv("athlete_events.csv")

# -----------------------------
# Étapes auxiliaires
# -----------------------------


# Correction des données pour distinguer les épreuves individuelles et collectives,
# onn suppose qu’une épreuve est collective si elle attribue ≥ 6 médailles
def ajouter_type_epreuve(donnees):
    corrected_rows = []
    for event, group in donnees.groupby("Event"):
        medal_counts = group["Medal"].value_counts()
        total_medals = medal_counts.sum()

        if total_medals >= 6:
            kept_medals = []
            for medal in ["Gold", "Silver", "Bronze"]:
                if medal in group["Medal"].values:
                    first_occurrence = group[group["Medal"] == medal].iloc[[0]]
                    kept_medals.append(first_occurrence)
            if kept_medals:
                corrected_rows.append(pd.concat(kept_medals))
        else:
            corrected_rows.append(group)

    donnees_corr = pd.concat(corrected_rows, ignore_index=True)
    donnees_corr["Type"] = "individuel"
    epreuves_collectives = donnees_corr["Event"].value_counts()
    epreuves_collectives = epreuves_collectives[epreuves_collectives >= 6].index
    donnees_corr.loc[donnees_corr["Event"].isin(epreuves_collectives), "Type"] = (
        "collectif"
    )
    return donnees_corr


# Chaque ligne représente une épreuve. Pour chaque épreuve, on calcule des variables
# statistiques qui vont servir de caractéristiques pour la classification
def construire_table_epreuves(donnees):
    table = donnees.groupby("Event").agg(
        {
            "Sport": "first",
            "ID": "nunique",
            "NOC": "nunique",
            "Sex": lambda x: (x == "F").sum() / len(x),
            "Age": ["mean", "std"],
            "Weight": ["mean", "std"],
            "Height": ["mean", "std"],
            "Year": "min",
            "Type": "first",
        }
    )

    table.columns = [
        "Sport",
        "Nb participants",
        "Nb pays",
        "Part femmes",
        "Âge moyen",
        "Écart âge",
        "Poids moyen",
        "Écart poids",
        "Taille moyenne",
        "Écart taille",
        "Année apparition",
        "Type",
    ]
    table = table.reset_index()
    table["Nb épreuves dans le sport"] = table.groupby("Sport")["Event"].transform(
        "count"
    )
    table["Type collectif"] = (table["Type"] == "collectif").astype(int)
    return table

# -----------------------------
# Traitement par période
# -----------------------------
# les statistiques qui vont servir de caractéristiques (features) pour la classification
colonnes_features = [
    "Nb participants",
    "Part femmes",
    "Âge moyen",
    "Écart âge",
    "Poids moyen",
    "Écart poids",
    "Taille moyenne",
    "Écart taille",
]


# écoupage en 4 périodes de 25 ans
periodes = {
    "1916-1940": (1916, 1940),
    "1941-1965": (1941, 1965),
    "1966-1990": (1966, 1990),
    "1991-2016": (1991, 2016),
}

# Classification K-means (non supervisée)

# Pour chaque période
tables_par_periode = []
# On normalise les variables
scaler = StandardScaler()

# On applique K-means avec 4 clusters (groupes)
for nom_periode, (debut, fin) in periodes.items():
    print(f"→ Traitement de la période {nom_periode}")
    subset = df[(df["Year"] >= debut) & (df["Year"] <= fin)].copy()
    subset = ajouter_type_epreuve(subset)
    table = construire_table_epreuves(subset)
    table["Période"] = nom_periode

    # Nettoyage
    table = table.dropna(subset=colonnes_features)
    X_scaled = scaler.fit_transform(table[colonnes_features])

    # KMeans
    kmeans = KMeans(n_clusters=3, random_state=0)
    table["Cluster"] = kmeans.fit_predict(X_scaled)

    tables_par_periode.append(table)

# -----------------------------
# PCA sur toutes les périodes
# -----------------------------
table_periodes = pd.concat(tables_par_periode, ignore_index=True)
X_scaled_all = scaler.fit_transform(table_periodes[colonnes_features])
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled_all)

table_periodes["Dim1"] = X_pca[:, 0]
table_periodes["Dim2"] = X_pca[:, 1]


# -----------------------------
# Visualisation PCA
# -----------------------------
# Chaque point dans le plan PCA représente une épreuve
sns.set(style="whitegrid")
g = sns.relplot(
    data=table_periodes,
    x="Dim1",
    y="Dim2",
    hue="Cluster",
    col="Période",
    palette="tab10",
    kind="scatter",
    height=5,
    aspect=1,
)
g.fig.suptitle(
    "Classification des épreuves sportives par période (PCA + K-means)", y=1.05
)
plt.tight_layout()
plt.savefig("pca_clusters_par_periode.png")
plt.show()


# Affiche les contributions des variables aux deux premiers axes PCA
pca_components = pd.DataFrame(
    pca.components_,
    columns=colonnes_features,  # les noms des variables originales
    index=["Dim1", "Dim2"],
)

print("Contribution des variables aux axes  :")
print(pca_components.T.sort_values("Dim1", ascending=False))  # trier pour voir l'impact

# stat desc
# Fusionner les données avec leur cluster
data_clustered = table_periodes.copy()

# Moyenne de chaque variable par cluster
cluster_summary = data_clustered.groupby("Cluster")[colonnes_features].mean().round(2)
print("Résumé statistique par cluster :")
print(cluster_summary)

# Écart-type
cluster_std = data_clustered.groupby("Cluster")[colonnes_features].std().round(2)

# export excel
with pd.ExcelWriter("resume_clusters.xlsx") as writer:
    cluster_summary.to_excel(writer, sheet_name="Moyennes")
    cluster_std.to_excel(writer, sheet_name="Ecart-type")


# profils moyens pas cluster
def interpreter_cluster(cluster_id, summary):
    ligne = summary.loc[cluster_id]
    texte = f"Cluster {cluster_id} :\n"
    if ligne["Nb participants"] > 50:
        texte += "- Épreuves très fréquentées\n"
    if ligne["Part femmes"] > 0.6:
        texte += "- Majoritairement féminines\n"
    if ligne["Poids moyen"] > 75:
        texte += "- Athlètes lourds\n"
    if ligne["Taille moyenne"] > 180:
        texte += "- Athlètes de grande taille\n"
    if ligne["Année apparition"] > 2000:
        texte += "- Épreuves récentes\n"
    if ligne["Type collectif"] == 1:
        texte += "- Épreuves collectives\n"
    else:
        texte += "- Épreuves individuelles\n"
    return texte


# -----------------------------
# Export Excel
# -----------------------------
table_periodes.to_excel("classification_epreuves_olympiques.xlsx", index=False)
print("✅ Export Excel terminé : classification_epreuves_olympiques.xlsx")
