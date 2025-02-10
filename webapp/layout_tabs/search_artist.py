from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from layout_tabs.utils import search_elasticsearch, get_artist_details


def get_layout():
    return dbc.Container(
        [
            html.H2("🔍 Recherche par Artiste", className="text-center mb-4"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Input(
                            id="artist-search",
                            type="text",
                            placeholder="Entrez un artiste...",
                            debounce=True,
                            className="form-control",
                        ),
                        width=8,
                    ),
                    dbc.Col(
                        dbc.Button("Rechercher", id="artist-search-btn", color="primary", className="btn-block"),
                        width=4,
                    ),
                ],
                className="mb-3",
            ),
            html.Div(id="artist-results"),
        ],
        className="p-4",
    )

def register_callbacks(app):
    @app.callback(
        Output("artist-results", "children"),
        Input("artist-search-btn", "n_clicks"),
        Input("artist-search", "value"),
    )
    def update_results(n_clicks, artist_name):
        if not artist_name:
            return "Veuillez entrer un artiste."

        results = get_artist_details(artist_name)

        if isinstance(results, str):
            return results  # Aucun résultat trouvé
        # Définition des colonnes avec des emojis 🏆🎶🏷️📅
        columns = {
            "artiste": "🎤 Artiste",
            "album": "💿 Album",
            "label": "🏷️ Label",
            "date_sortie": "📅 Date de sortie",
            "certification": "🏆 Certification",
            "date_certification": "📅 Date Certification",
        }

        return dbc.Table(
            [
                html.Thead(html.Tr([html.Th(col, style={"fontWeight": "bold", "textAlign": "center"}) for col in columns.values()])),
                html.Tbody([
                    html.Tr([html.Td(row[key], style={"textAlign": "center"}) for key in columns.keys()])
                    for row in results
                ])
            ],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            style={"marginTop": "20px", "width": "100%"},
        )
