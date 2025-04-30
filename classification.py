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


def construire_table_epreuves(donnees):
    table = (
        donnees.groupby("Event")
        .agg(
            **{
                "Sport": ("Sport", "first"),
                "Nb participants": ("ID", "nunique"),
                "Nb pays": ("NOC", "nunique"),
                "Part femmes": ("Sex", lambda x: (x == "F").sum() / len(x)),
                "Âge moyen": ("Age", "mean"),
                "Écart âge": ("Age", "std"),
                "Poids moyen": ("Weight", "mean"),
                "Écart poids": ("Weight", "std"),
                "Taille moyenne": ("Height", "mean"),
                "Écart taille": ("Height", "std"),
                "Année apparition": ("Year", "min"),
                "Type": ("Type", "first"),
            }
        )
        .reset_index()
    )
    table["Nb épreuves dans le sport"] = table.groupby("Sport")["Event"].transform(
        "count"
    )
    return table


# -----------------------------
# Traitement par période
# -----------------------------
colonnes_features = [
    "Nb épreuves dans le sport",
    "Nb participants",
    "Nb pays",
    "Part femmes",
    "Âge moyen",
    "Écart âge",
    "Poids moyen",
    "Écart poids",
    "Taille moyenne",
    "Écart taille",
]

periodes = {
    "1916-1940": (1916, 1940),
    "1941-1965": (1941, 1965),
    "1966-1990": (1966, 1990),
    "1991-2016": (1991, 2016),
}

tables_par_periode = []
scaler = StandardScaler()

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
    kmeans = KMeans(n_clusters=4, random_state=0)
    table["Cluster"] = kmeans.fit_predict(X_scaled)

    tables_par_periode.append(table)

# -----------------------------
# PCA sur toutes les périodes
# -----------------------------
table_periodes = pd.concat(tables_par_periode, ignore_index=True)
X_scaled_all = scaler.fit_transform(table_periodes[colonnes_features])
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled_all)

table_periodes["PCA1"] = X_pca[:, 0]
table_periodes["PCA2"] = X_pca[:, 1]

# -----------------------------
# Visualisation PCA
# -----------------------------
sns.set(style="whitegrid")
g = sns.relplot(
    data=table_periodes,
    x="PCA1",
    y="PCA2",
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

# -----------------------------
# Export Excel
# -----------------------------
table_periodes.to_excel("classification_epreuves_olympiques.xlsx", index=False)
print("✅ Export Excel terminé : classification_epreuves_olympiques.xlsx")
