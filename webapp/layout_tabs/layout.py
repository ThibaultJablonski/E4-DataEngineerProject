import dash_bootstrap_components as dbc
from dash import dcc, html

def snep_footer():
    return html.Footer(
        [
            html.P("Avec l'aide du site de :", className="text-center", style={"fontSize": "14px"}),
            html.Div(html.Img(src="/assets/snep_logo.png", height="40px"), className="text-center"),
        ],
        className="footer mt-auto py-3",
        style={"position": "relative", "bottom": "0", "width": "100%", "textAlign": "center"},
    )

def create_layout():
    return html.Div(
        [
            dbc.Navbar(
                dbc.Container(
                    [
                        # 🔹 Lien "Thibault²" à gauche
                        dbc.NavbarBrand(
                            html.A("Thibault²", href="/", className="navbar-home-link"),
                            className="mr-auto",
                        ),

                        # 🔹 Titre centré
                        # 🔹 Titre stylisé avec image de fond
                        html.Div(
                            style={
                                "backgroundImage": "url('/assets/banner.png')",
                                "backgroundSize": "cover",
                                "padding": "40px",
                                "textAlign": "center",
                                "borderRadius": "10px",
                            },
                            children=[
                                html.H1(
                                    "Certifications SNEP | Découverte",
                                    style={
                                        "color": "white",
                                        "fontSize": "42px",
                                        "fontWeight": "bold",
                                        "textShadow": "2px 2px 4px rgba(0,0,0,0.4)",
                                    },
                                ),
                            ],
                        ),


                        # 🔹 Liens à droite
                        dbc.Nav(
                            [
                                dbc.DropdownMenu(
                                    label="Recherche 🔎",
                                    nav=True,
                                    in_navbar=True,
                                    children=[
                                        dbc.DropdownMenuItem("Par Artiste", href="/search_artist"),
                                        dbc.DropdownMenuItem("Par Album", href="/search_album"),
                                        dbc.DropdownMenuItem("Par Label", href="/search_label"),
                                    ],
                                ),
                                dbc.NavItem(dbc.NavLink("À propos ℹ️", href="/about")),
                            ],
                            className="ml-auto",
                            navbar=True,
                        ),
                    ],
                    fluid=True,
                    className="d-flex justify-content-between align-items-center",
                ),
                color="dark",
                dark=True,
                className="mb-4",
            ),

            html.Div(id="page-content", className="content"),

            snep_footer(),  # 📌 Footer ajouté ici
        ],
        className="d-flex flex-column min-vh-100",  # 🔥 CSS pour pousser le footer en bas
    )
