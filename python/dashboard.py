'''
Dashboard
'''
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import json
from frequent_keywords import frequent_keywords_hist 
from mentioned_countries import mentionned_countries_map
from articles_per_month import articles_per_month
from flask import Flask, send_from_directory


def generate_dashboard(html_files):

    #Create the dash app
    app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], title='Corpus Data Analysis Dashboard')
    
    server = app.server
    #Configure path
    @server.route('/graphes/<path:filename>')
    def serve_html(filename):
        return send_from_directory('graphes', filename)

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
                        options = [{'label': file['label'][20:-5], 'value' : file['label']}
                                    for file in html_files],
                        value = html_files[0]['label'],
                        optionHeight=60,
                        className='customDropdown')
                        ],
                style={
                    'margin-top': '7vh',
                    'margin-left': '0.4vw',
                    'margin-right': '0.4vw'
                    }
            ),
            html.Div([
                html.H2("View the graph"),
                dbc.Button("Open it", 
                    id='open-button',
                    href=f'/graphes/{html_files[0]["value"]}',
                    className="custom-button", 
                    target="_blank",
                    style ={
                    'width': '90%',
                    'align-items' : 'center'
                    }
                )],
                style={
                    'width': '100%',
                    'margin-top': '7vh',
                    'margin-left': '0.4vw',
                    'margin-right': '0.4vw'
                }),
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


    # Callback for update graphics
    @app.callback(
        Output(component_id="graphs-container", component_property="children"),
        Input(component_id="dataset", component_property="value"),
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
        
    # Callback 2: Update link on the button
    @app.callback(
        Output('open-button', 'href'),
        Input('dataset', 'value')
    )
    def update_button_url(selected_file):
        value = [item['value'] for item in html_files if item['label'] == selected_file]
        return f"/graphes/{value[0]}"

    return app
    




    