from dash import html
import dash_bootstrap_components as dbc

# Sidebar avec boutons pour naviguer entre les pages
sidebar = html.Div([
    html.H2("Navigation"),
    dbc.Button("Tableau de bord", id="btn-dashboard", n_clicks=0),
    dbc.Button("Dépenses", id="btn-expenses", n_clicks=0),
    dbc.Button("Gestion budgétaire", id="btn-budget", n_clicks=0),
    dbc.Button("Revenus", id="btn-income", n_clicks=0),
], style={'width': '15%', 'float': 'left', 'padding': '20px'})
