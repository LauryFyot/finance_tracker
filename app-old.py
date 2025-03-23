# import dash
# from dash import dcc, html, Input, Output
# import plotly.express as px
# import pandas as pd
# import dash_bootstrap_components as dbc


# # Charger les données (remplace avec le bon chemin si nécessaire)
# file_path = "data/bnp_export_15_03.xlsx"
# df = pd.read_excel(file_path)

# df["Date operation"] = pd.to_datetime(df["Date operation"])
# df_expenses = df[df["Montant operation"] < 0]
# df_income = df[df["Montant operation"] > 0]

# # Graphiques pour chaque page
# # Page 1 - Tableau de bord
# category_expenses = df_expenses.groupby("Categorie operation")["Montant operation"].sum().reset_index()
# category_expenses["Montant operation"] = category_expenses["Montant operation"].abs()
# fig_pie = px.pie(category_expenses, names="Categorie operation", values="Montant operation", title="Répartition des dépenses")

# daily_expenses = df_expenses.groupby("Date operation")["Montant operation"].sum().reset_index()
# fig_line = px.line(daily_expenses, x="Date operation", y="Montant operation", title="Évolution des dépenses", markers=True)

# # Page 2 - Analyse des dépenses
# top_expenses = df_expenses.nsmallest(10, "Montant operation")
# fig_top_exp = px.bar(top_expenses, x="Montant operation", y="Libelle operation", orientation="h", title="Top 10 des plus grosses dépenses")

# # Page 4 - Analyse des revenus
# daily_income = df_income.groupby("Date operation")["Montant operation"].sum().reset_index()
# fig_income_line = px.line(daily_income, x="Date operation", y="Montant operation", title="Évolution des revenus", markers=True)






# # Application Dash
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# app.layout = html.Div([
#     # Sidebar à gauche
#     html.Div([
#         html.H2("Navigation"),
#         html.Button("Tableau de bord", id="btn-dashboard", n_clicks=0),
#         html.Button("Analyse des dépenses", id="btn-expenses", n_clicks=0),
#         html.Button("Gestion budgétaire", id="btn-budget", n_clicks=0),
#         html.Button("Analyse des revenus", id="btn-income", n_clicks=0),
#     ], style={'width': '20%', 'float': 'left', 'padding': '20px'}),

#     # Contenu dynamique (à droite)
#     html.Div(id='content', style={'width': '80%', 'float': 'right', 'padding': '20px'})
# ])

# # Callback pour mettre à jour la page affichée
# @app.callback(
#     Output('content', 'children'),
#     [Input('btn-dashboard', 'n_clicks'),
#      Input('btn-expenses', 'n_clicks'),
#      Input('btn-budget', 'n_clicks'),
#      Input('btn-income', 'n_clicks')]
# )

# def display_page(dash_click, exp_click, budget_click, income_click):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return html.Div([dcc.Graph(figure=fig_pie), dcc.Graph(figure=fig_line)])
#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
#     if button_id == "btn-expenses":
#         return html.Div([dcc.Graph(figure=fig_pie), dcc.Graph(figure=fig_top_exp)])
#     elif button_id == "btn-budget":
#         return html.Div([html.H3("Gestion budgétaire - À implémenter")])
#     elif button_id == "btn-income":
#         return html.Div([dcc.Graph(figure=fig_income_line)])
#     else:
#         return html.Div([dcc.Graph(figure=fig_pie), dcc.Graph(figure=fig_line)])

# if __name__ == '__main__':
#     app.run_server(debug=True, port=9090)







# Fonctionnel mais bcp plus simple

# def get_operations_table(selected_category, start_date, end_date):
#     # Filtrer les données par date
#     df_filtered = df_expenses[
#         (df_expenses["Date operation"] >= start_date) &
#         (df_expenses["Date operation"] <= end_date)
#     ]
    
#     # Si une catégorie spécifique est sélectionnée, appliquer le filtre
#     if selected_category != "All":
#         df_filtered = df_filtered[df_filtered["Categorie operation"] == selected_category]
    
#     # Trier par date décroissante et prendre les 10 dernières opérations
#     df_filtered = df_filtered.sort_values("Date operation", ascending=False)

#     return html.Div([
#         dash_table.DataTable(
#             id="operations-table",
#             columns=[
#                 {"name": "Date", "id": "Date operation"},
#                 {"name": "Libellé", "id": "Libelle operation"},
#                 {"name": "Montant", "id": "Montant operation"},
#             ],
#             data=df_filtered.to_dict("records"),
            
#             # ✅ Fixe la hauteur et permet le scroll vertical dans la table
#             style_table={'height': '400px', 'overflowY': 'auto', 'width': '100%'},  
            
#             style_header={'backgroundColor': 'black', 'color': 'white', 'fontWeight': 'bold'},
#             style_data={'backgroundColor': '#222', 'color': 'white'},
            
#             style_data_conditional=[
#                 {'if': {'row_index': 'odd'}, 'backgroundColor': '#333'},  # Alternance des couleurs
#                 {'if': {'column_id': 'Libelle operation'},  
#                 'whiteSpace': 'normal', 'textAlign': 'left', 'maxWidth': '300px', 'overflow': 'hidden'}
#             ],
#             style_cell={'padding': '10px'},  # Espacement interne des cellules
#             style_cell_conditional=[
#                 {'if': {'column_id': 'Date operation'}, 'width': '15%', 'textAlign': 'center'},
#                 {'if': {'column_id': 'Libelle operation'}, 'width': '50%'},
#                 {'if': {'column_id': 'Montant operation'}, 'width': '15%', 'textAlign': 'right'},
#             ],
#             css=[{"selector": "tr:hover", "rule": "background-color: #444 !important;"}],  # Effet hover
#             filter_action="native",  # Barre de recherche activée
#             sort_action="native"  # Activation du tri dynamique
#         ),
#         html.Button("Exporter en CSV", id="export-csv", n_clicks=0, style={'margin-top': '10px'})
#     ])    