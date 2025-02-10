import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import socket
from layout_tabs.layout import create_layout
from layout_tabs.search_artist import get_layout as artist_layout, register_callbacks as artist_callbacks
from layout_tabs.search_album import get_layout as album_layout, register_callbacks as album_callbacks
from layout_tabs.search_label import get_layout as label_layout, register_callbacks as label_callbacks
from layout_tabs.about import get_layout as about_layout

# Initialisation de l'application avec Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    create_layout()
])
#  Enregistrement des callbacks pour chaque module
artist_callbacks(app)
album_callbacks(app)
label_callbacks(app)

#  Callback pour afficher le bon contenu selon la page
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/search_artist":
        return artist_layout()
    elif pathname == "/search_album":
        return album_layout()
    elif pathname == "/search_label":
        return label_layout()
    elif pathname == "/about":
        return about_layout()
    else:
        return dbc.Container(
        [
            html.H2("🎵 Bienvenue sur le Dashboard SNEP !", 
                    className="text-center mt-4 text-primary"),

            html.P(
                "🔍 Pour rechercher vos artistes préférés ou vos labels préférés, cliquez sur l'onglet 'Recherche' en haut à droite.",
                className="text-center font-weight-bold",
                style={"fontSize": "18px", "marginTop": "20px"},
            ),

            html.Img(src="/assets/music_search.png", 
                    style={"display": "block", "margin": "auto", "width": "10%"}),  # Ajout d'une image si tu veux
            
            html.P(
                "Découvrez les certifications et albums des artistes français et internationaux depuis 2016.",
                className="text-center",
                style={"fontSize": "16px", "marginTop": "10px"},
            ),
        ],
        className="text-center mt-4",
    )



if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    local_ip = socket.gethostbyname(socket.gethostname())

    print(f"Application disponible sur : http://localhost:{port}")

    app.run(host=host, port=port, debug=True)
