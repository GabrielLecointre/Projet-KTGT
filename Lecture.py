import pandas

# Read myData.xlsx Excel file
df = pandas.read_excel(r"myData.xlsx")

# Display all the data from myData.xlsx Excel file
print("* Tableau Excel du fichier myData.xlsx :")
print(df)
