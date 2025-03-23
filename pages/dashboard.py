from dash import html, dcc, dash_table
import plotly.express as px
from data_loader import df, df_expenses, df_income, json_accounts
from utils.theme import apply_dark_theme
import pandas as pd
import dash_bootstrap_components as dbc


df_expenses_grouped = df_expenses.groupby("Année-Mois")["Montant operation"].sum().reset_index()
df_expenses_grouped.rename(columns={"Montant operation": "Dépenses"}, inplace=True)
df_income_grouped = df_income.groupby("Année-Mois")["Montant operation"].sum().reset_index()
df_income_grouped.rename(columns={"Montant operation": "Revenus"}, inplace=True)
df_grouped = pd.merge(df_expenses_grouped, df_income_grouped, on="Année-Mois", how="outer").fillna(0)
df_grouped["Économie"] = (df_grouped["Revenus"] - df_grouped["Dépenses"]).round(2)
df_grouped["Année-Mois"] = df_grouped["Année-Mois"].astype(str)
fig_evolution = px.line(df_grouped, x="Année-Mois", 
                        y=["Dépenses", "Revenus"],
                        title="Évolution des Dépenses et Revenus par Mois",
                        markers=True, 
                        line_shape="spline",
                        hover_data={"Économie": True})
fig_evolution.update_layout(yaxis_ticksuffix="€",
                            legend_title_text="",
                            xaxis_title=None,
                            yaxis_title=None)


# Graphique des catégories
category_expenses = df_expenses.groupby("Categorie operation")["Montant operation"].sum().reset_index()
category_expenses["Montant operation"] = category_expenses["Montant operation"].abs()
fig_pie = px.pie(category_expenses, names="Categorie operation", values="Montant operation",
                     title="Répartition des dépenses", hole=0.4)
fig_pie.update_layout(
    legend=dict(
        orientation="h",  # Légende verticale
        yanchor="middle",
        y=0.5,
        xanchor="center",
        x=1.2,
        traceorder="normal"
    )
)



# Scorecards
scorecards = [
    dbc.Card(dbc.CardBody([html.H4("💰 Compte chèques", className="card-title"), html.P(f"{json_accounts['compte_cheque']} €", className="card-text")]), color="primary", inverse=True),
    dbc.Card(dbc.CardBody([html.H4("📊 Compte épargne", className="card-title"), html.P(f"{json_accounts['compte_epargne']} €", className="card-text")]), color="success", inverse=True),
    dbc.Card(dbc.CardBody([html.H4("📉 Livret Durable", className="card-title"), html.P(f"{json_accounts['livret_dev_durable']} €", className="card-text")]), color="danger", inverse=True),
    dbc.Card(dbc.CardBody([html.H4("🔄 Livret Jeune", className="card-title"), html.P(f"{json_accounts['livret_jeune']} €", className="card-text")]), color="info", inverse=True)
]

# Layout avec grille Bootstrap
layout = dbc.Container([
    # Ligne des 4 scorecards
    dbc.Row([
        dbc.Col(card, width=3) for card in scorecards
    ], className="mb-4"),

    # Ligne avec le graphe d'évolution (3 colonnes, 2 hauteurs) et le pie chart (1 colonne, 2 hauteurs)
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_evolution), width=7, style={"height": "400px"}),  # 3 colonnes sur 4
        dbc.Col(dcc.Graph(figure=fig_pie), width=5, style={"height": "400px"})  # 1 colonne sur 4
    ])
], fluid=True)


# # Layout de la page Tableau de Bord
# layout = html.Div([
#     html.H3("Tableau de Bord"),
# ])