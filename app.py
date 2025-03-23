import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from layouts import sidebar
from callbacks import register_callbacks

# Initialisation de l'application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
app.title = "Finance Tracker"

# Layout principal avec sidebar + contenu dynamique
app.layout = html.Div([
    sidebar,  # Sidebar fixe à gauche
    html.Div(id="content", style={
        'width': '85%',
        'float': 'right',
        'padding': '20px',
        'height': '100vh',  # Hauteur 100% de l'écran
        'overflow-y': 'auto',  # Active le scroll vertical UNIQUEMENT ici
        # 'background-color': '#111'  # Fond sombre pour s'intégrer au dark mode
    })
])


# Enregistrer les callbacks (navigation entre pages)
register_callbacks(app)

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True, port=9090)
