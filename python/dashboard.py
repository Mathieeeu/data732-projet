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
                html.P("This dashboard allows to view data extracted from different articles coming from site of extreme right ")
                ]), 
            html.Div([
                html.H2("Choose a soucre of data"),
                dcc.Dropdown(id="dataset",
                        options = [{'label': file[20:-5], 'value' : file}
                                    for file in file_list],
                        value = file_list[0],
                        optionHeight=80,
                        className='customDropdown')
                        ],
                style={
                    'margin-top': 100,
                    'margin-left': 15,
                    'margin-right': 15
                    }
            ),
            html.Div(
                html.P("@ Louna Camas & Mathieu Docher, All rights reserved"),
                style ={
                    'color' : '#cccccc',
                    'font-size' : '5px',
                    'margin-top' : '33vh'}), 
            ],
            style={
                'width': '15%',
                'margin-left': 15,
                'margin-top': 35,
                'margin-bottom': 35
                }),
        html.Div(
            id="graphs-container", 
            className="graphs-container",
            style={
                'width': '100%',
                'margin-top': 35,
                'margin-right': 35,
                'margin-bottom': 35,
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
                html.Div(dcc.Graph(figure=fig_frequent_keywords), className="graph-div graph-1"),
                html.Div(dcc.Graph(figure=fig_articles_per_month), className="graph-div graph-3"),
                html.Div(dcc.Graph(figure=fig_country_map), className="graph-div graph-4"),
                html.Div(dcc.Graph(figure=fig_country_hist), className="graph-div graph-2"),
            ],
            className="grid-container"
        )

    return app
    




    