import pandas as pd
import json

with open("data/comptes.json", "r", encoding="utf-8") as fichier:
    comptes = json.load(fichier)

def load_data():
    file_path = "data/bnp_export_15_03.xlsx"
    df = pd.read_excel(file_path)
    df["Date operation"] = pd.to_datetime(df["Date operation"])
    return df

df = load_data()
df["Année-Mois"] = df["Date operation"].dt.to_period("M")


# Filtrer uniquement les dépenses
df_expenses = df
df_expenses = df_expenses[df_expenses["Montant operation"] < 0]
df_expenses = df_expenses[df_expenses["Sous Categorie operation"] != 'Virement interne']
df_expenses = df_expenses[df_expenses["Categorie operation"] != 'Revenus']
df_expenses["Montant operation"] = df_expenses["Montant operation"].abs()  # Valeur absolue

# Filtrer uniquement les revenus
df_income = df[df["Montant operation"] > 0]

# Récupérer l'état des comptes
json_accounts = comptes
