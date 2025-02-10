from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from layout_tabs.utils import get_album_details


def get_layout():
    return dbc.Container(
        [
            html.H2("🔍 Recherche par Album", className="text-center mb-4"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Input(
                            id="album-search",
                            type="text",
                            placeholder="Entrez un album...",
                            debounce=True,
                            className="form-control",
                        ),
                        width=8,
                    ),
                    dbc.Col(
                        dbc.Button("Rechercher", id="album-search-btn", color="primary", className="btn-block"),
                        width=4,
                    ),
                ],
                className="mb-3",
            ),
            html.Div(id="album-results"),
        ],
        className="p-4",
    )


def register_callbacks(app):
    @app.callback(
        Output("album-results", "children"),
        Input("album-search-btn", "n_clicks"),
        Input("album-search", "value"),
    )
    def update_results(n_clicks, album_name):
        if not album_name:
            return "Veuillez entrer un album."

        results = get_album_details(album_name)

        if isinstance(results, str):
            return results  # Aucun résultat trouvé

        # Définition des colonnes avec des emojis 🎤💿🏷️📅🏆
        columns = {
            "album": "💿 Album",
            "artiste": "🎤 Artiste",
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
