import dash
from dash import html, dcc, Input, Output
from pages import dashboard, expenses, budget, income
from pages.expenses import get_dashboard_graphs, get_operations_table  # Import de la fonction qui génère les graphiques dynamiques
from data_loader import df_expenses
import dash_bootstrap_components as dbc

def register_callbacks(app):
    # Callback pour changer de page
    @app.callback(
        Output('content', 'children'),
        [Input('btn-dashboard', 'n_clicks'),
         Input('btn-expenses', 'n_clicks'),
         Input('btn-budget', 'n_clicks'),
         Input('btn-income', 'n_clicks')]
    )
    def display_page(dash_click, exp_click, budget_click, income_click):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dashboard.layout  # Page d'accueil par défaut
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == "btn-expenses":
            return expenses.layout
        elif button_id == "btn-budget":
            return budget.layout
        elif button_id == "btn-income":
            return income.layout
        else:
            return dashboard.layout

    # Callback pour filtrer les données du Tableau de Bord en fonction des dates sélectionnées
    @app.callback(
        Output("dashboard-graphs", "children"),
        [Input("date-picker-dashboard", "start_date"),
         Input("date-picker-dashboard", "end_date")]
    )
    def update_dashboard(start_date, end_date):
        return get_dashboard_graphs(start_date, end_date)  # Générer les nouveaux graphiques
    

    @app.callback(
        Output("operations-table-container", "children"),  # Met à jour la Div entière
        [Input("category-dropdown", "value"),
         Input("date-picker-dashboard", "start_date"),
         Input("date-picker-dashboard", "end_date")]
    )
    def update_operations_table(selected_category, start_date, end_date):        
        return get_operations_table(selected_category, start_date, end_date)  # Retourne un DataTable mis à jour