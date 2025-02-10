from dash import html, dcc
import dash_bootstrap_components as dbc

def get_layout():
    """ Page À propos du projet """
    return dbc.Container(
        [
            html.H2("ℹ️ À propos du projet", className="text-center mb-4"),
            
            html.P(
                "Ce projet est une plateforme permettant d'explorer les certifications d'albums en France "
                "grâce aux données de la SNEP. Il utilise le web scraping, Elasticsearch pour la recherche et la création de base de données, et "
                "Dash pour l'affichage interactif.",
                className="lead text-center"
            ),

            html.Hr(),

            html.H3("🚀 Technologies utilisées"),
            dbc.Row(
                [
                    dbc.Col(html.Div("🕸️ Web Scraping avec Scrapy"), width=4),
                    dbc.Col(html.Div("🔎 Elasticsearch pour la recherche et base de données"), width=4),
                    dbc.Col(html.Div("📊 Dash pour la visualisation"), width=4),
                ],
                className="mb-4 text-center",
            ),

            html.H3("👨‍💻 Développement"),
            html.P(
                "Cette interface a été réalisé dans le cadre d'un projet de Data Engineering (scraping et de visualisation de données), "
                "avec une approche orientée microservices via Docker.",
                className="text-center"
            ),

            html.Hr(),

            html.H3("Créateur du Dashboard"),
            html.P(
                "Créé par Thibault Jablonski et Thibault Le Guidevais",
                className="text-center"
            ),

            # 📷 Ajout des images
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="/assets/IMG_3050.png", height="150px"), width=6),
                            dbc.Col(html.Img(src="/assets/IMG_4289.png", height="150px"), width=6),
                        ],
                        justify="center",
                    )
                ],
                className="text-center mt-4",
            ),
        ],
        className="p-4",
    )
