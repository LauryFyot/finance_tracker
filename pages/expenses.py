from dash import html, dcc, dash_table
import plotly.express as px
from data_loader import df_expenses
from utils.theme import apply_dark_theme
import pandas as pd

# Composant pour sélectionner la plage de dates
date_picker = dcc.DatePickerRange(
    id="date-picker-dashboard",
    start_date=df_expenses["Date operation"].min(),  
    end_date=df_expenses["Date operation"].max(),  
    display_format="DD/MM/YYYY",
    start_date_placeholder_text="Début",
    end_date_placeholder_text="Fin"
)

# Dropdown pour sélectionner une catégorie
category_dropdown = dcc.Dropdown(
    id="category-dropdown",
    options=[{"label": "Toutes les catégories", "value": "All"}] + 
            [{"label": cat, "value": cat} for cat in df_expenses["Categorie operation"].unique()],
    value="All",  # Valeur par défaut
    clearable=False,
    style={'width': '50%'}
)

def get_operations_table(selected_category, start_date, end_date):
    # Filtrer les données par catégorie et plage de dates
    df_filtered = df_expenses[
        (df_expenses["Date operation"] >= start_date) &
        (df_expenses["Date operation"] <= end_date)
    ]
    
    if selected_category != "All":
        df_filtered = df_filtered[df_filtered["Categorie operation"] == selected_category]
    
    # Trier par date décroissante et prendre les 10 dernières opérations
    df_filtered = df_filtered.sort_values("Date operation", ascending=False)

    # ✅ Calculer le total
    total_montant = df_filtered["Montant operation"].sum()
    
    return html.Div([
        # ✅ Tableau principal avec scrollbar
        dash_table.DataTable(
            id="operations-table",
            columns=[
                {"name": "Date", "id": "Date operation"},
                {"name": "Libellé", "id": "Libelle operation"},
                {"name": "Montant", "id": "Montant operation", "type": "numeric"},
            ],
            data=df_filtered.astype(str).to_dict("records"),
            style_table={'height': '400px', 'overflowY': 'auto', 'width': '100%'},  # ✅ Scroll vertical
            style_header={'backgroundColor': 'black', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': '#222', 'color': 'white'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#333'},
                {'if': {'column_id': 'Libelle operation'},  
                 'whiteSpace': 'normal', 'textAlign': 'left', 'maxWidth': '300px', 'overflow': 'hidden'},
            ],
            style_cell={'padding': '10px'},
            style_cell_conditional=[
                {'if': {'column_id': 'Date operation'}, 'width': '15%', 'textAlign': 'center'},
                {'if': {'column_id': 'Libelle operation'}, 'width': '50%'},
                {'if': {'column_id': 'Montant operation'}, 'width': '15%', 'textAlign': 'right'},
            ],
            css=[{"selector": "tr:hover", "rule": "background-color: #444 !important;"}],  
            filter_action="native",  
            sort_action="native"  
        ),

        # ✅ Tableau du total FIXÉ en bas
        html.Div([
            dash_table.DataTable(
                id="operations-total",
                columns=[
                    {"name": "Date", "id": "Date operation"},
                    {"name": "Libellé", "id": "Libelle operation"},
                    {"name": "Montant", "id": "Montant operation", "type": "numeric"},
                ],
                data=[{"Date operation": "TOTAL", "Libelle operation": "", "Montant operation": total_montant}],
                style_table={'width': '100%', 'position': 'sticky', 'bottom': 0, 'backgroundColor': '#222'},
                style_header={'display': 'none'},  # ✅ Enlève l'en-tête du tableau du total
                style_data={'backgroundColor': '#444', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={
                    'fontFamily': 'Arial, sans-serif',  # Police personnalisée
                    'fontSize': '14px',  # Taille du texte
                    'padding': '10px',  # Espacement intérieur
                    'textAlign': 'left',  # Alignement du texte par défaut
                },
            )
        ], style={'position': 'sticky', 'bottom': 0, 'width': '100%'})  # ✅ Fixe le total en bas
    ])




# Fonction pour générer les graphiques
def get_dashboard_graphs(start_date, end_date):
    df_filtered = df_expenses[(df_expenses["Date operation"] >= start_date) & 
                              (df_expenses["Date operation"] <= end_date)]
    
    # Graphique des catégories
    category_expenses = df_filtered.groupby("Categorie operation")["Montant operation"].sum().reset_index()
    category_expenses["Montant operation"] = category_expenses["Montant operation"].abs()
    fig_pie = px.pie(category_expenses, names="Categorie operation", values="Montant operation",
                     title="Répartition des dépenses", hole=0.4)
    
    # Graphique d'évolution des dépenses
    daily_expenses = df_filtered.groupby("Date operation")["Montant operation"].sum().reset_index()
    fig_line = px.line(daily_expenses, x="Date operation", y="Montant operation", 
                       title="Évolution des dépenses", markers=True)
    
    # Appliquer le thème sombre
    apply_dark_theme(fig_pie)
    apply_dark_theme(fig_line)

    return [dcc.Graph(figure=fig_pie), dcc.Graph(figure=fig_line)]

# Layout de la page Tableau de Bord
layout = html.Div([
    html.H3("Tableau de Bord"),
    date_picker,  
    html.Div(id="dashboard-graphs"),  # Graphiques mis à jour
    html.Hr(),
    html.H4("Dernières opérations par catégorie"),
    category_dropdown,  
    html.Div(id="operations-table-container")  # Affichage du tableau
])