from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from layout_tabs.utils import get_certifications_by_label


def get_layout():
    return dbc.Container(
        [
            html.H2("🔍 Recherche par Label", className="text-center mb-4"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Input(
                            id="label-search",
                            type="text",
                            placeholder="Entrez un label...",
                            debounce=True,
                            className="form-control",
                        ),
                        width=8,
                    ),
                    dbc.Col(
                        dbc.Button("Rechercher", id="label-search-btn", color="primary", className="btn-block"),
                        width=4,
                    ),
                ],
                className="mb-3",
            ),
            html.Div(id="label-results"),
        ],
        className="p-4",
    )


def register_callbacks(app):
    @app.callback(
        Output("label-results", "children"),
        Input("label-search-btn", "n_clicks"),
        Input("label-search", "value"),
    )
    def update_results(n_clicks, label_name):
        if not label_name:
            return "Veuillez entrer un label."

        print(f"🚀 DEBUG: Recherche du label '{label_name}'")
        
        results = get_certifications_by_label(label_name)
        
        print(f"🔍 DEBUG: Résultat retourné par get_certifications_by_label : {results}")

        if isinstance(results, str):
            return results  # Aucun résultat trouvé

        # Définition des colonnes avec des emojis 
        columns = {
            "label": "🏷️ Label",
            "album": "💿 Album",
            "artiste": "🎤 Artiste",
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
