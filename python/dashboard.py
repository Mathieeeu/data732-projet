'''
Dashboard
'''
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import json
from frequent_keywords import frequent_keywords_hist 
from mentioned_countries import mentionned_countries_map
from articles_per_month import articles_per_month


def generate_dashboard(file_list):

    #Create the dash app
    app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], title='Corpus Data Analysis Dashboard')

    #Layout setup
    app.layout = dbc.Container([
        html.Div([
            html.Div([
                html.H1("Corpus Dashboard"),
                html.P("This dashboard provides an overview of data extracted from various articles published on far-right websites ")
                ]), 
            html.Div([
                html.H2("Choose a soucre of data"),
                dcc.Dropdown(id="dataset",
                        options = [{'label': file[20:-5], 'value' : file}
                                    for file in file_list],
                        value = file_list[0],
                        optionHeight=60,
                        className='customDropdown')
                        ],
                style={
                    'margin-top': '5vh',
                    'margin-left': '0.4vw',
                    'margin-right': '0.4vw'
                    }
            ),
            html.Div(
                html.P("@ Louna Camas & Mathieu Docher, All rights reserved",
                style ={
                    'color' : '#cccccc',
                    'font-size' : 12,
                    'margin-top' : '20vh'})), 
            ],
            style={
                'width': '15%',
                'margin-left': '0.4vw',
                'margin-top': '0.4vh',
                'margin-bottom': '5vh'
                }),
        html.Div(
            id="graphs-container", 
            className="graphs-container",
            style={
                'width': '100%',
                'margin-top': '5vh',
                'margin-right': '1vw',
                'margin-left': '1vw',
                'margin-bottom': '1vh',
                'display': 'flex'
            })
    ],
        fluid=True,
        style={'display': 'flex'},
        className='dashboard-container')


    # Callback function
    @app.callback(
        Output(component_id="graphs-container", component_property="children"),
        Input(component_id="dataset", component_property="value")
    )
    def update_graphs(selected_dataset):
        # Load dataset
        with open(selected_dataset, "r", encoding="utf-8") as f:
            data = json.loads(f.read())

        # Generate individual figures
        fig_frequent_keywords = frequent_keywords_hist(data)
        fig_country_hist, fig_country_map = mentionned_countries_map(data)
        fig_articles_per_month = articles_per_month(data)
        
        # Create separate divs for each figure
        return html.Div(
            children=[
                html.Div(dcc.Graph(figure=fig_frequent_keywords, style={"width": "30vw", "height": "45vh"}), className="graph-div graph-1"),
                html.Div(dcc.Graph(figure=fig_articles_per_month, style={"width": "30vw", "height": "45vh"}), className="graph-div graph-3"),
                html.Div(dcc.Graph(figure=fig_country_map, style={"width": "50vw", "height": "45vh"}), className="graph-div graph-4"),
                html.Div(dcc.Graph(figure=fig_country_hist, style={"width": "50vw", "height": "45vh"}), className="graph-div graph-2"),
            ],
            className="grid-container"
        )

    return app
    




    