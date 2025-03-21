import pandas

# Lire le fichier Excel avec la base de données
BDJO = pandas.read_excel(r"\\filer-eleves2\id2626\Downloads\BDProjetTD.xlsx")
print("* Tableau Excel du fichier :")
print(BDJO)
