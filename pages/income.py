from dash import html, dcc
import plotly.express as px
from data_loader import df_income
from utils.theme import apply_dark_theme

daily_income = df_income.groupby("Date operation")["Montant operation"].sum().reset_index()
fig_income_line = px.line(daily_income, x="Date operation", y="Montant operation", title="Évolution des revenus", markers=True)

apply_dark_theme(fig_income_line)

layout = html.Div([
    html.H3("Analyse des Revenus"),
    dcc.Graph(figure=fig_income_line),
])
