'''
Dashboard
'''
import json
import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
from frequent_keywords import frequent_keywords_hist 
from mentioned_countries import mentionned_countries_map
from plotly.subplots import make_subplots

# file_list = ["data/topaz-data732--france--www.fdesouche.com--20190101--20211231.json"]

def generate_data(file_list):
    """
    create a dict with file_name as key and its data as value
    """
    data = {}

    for file in file_list:
        f = open(file, "r", encoding="utf-8")
        data[file] = json.loads(f.read())
        f.close()

    return data


def generate_dashboard(file_list):
    #Create the dash app
    app = dash.Dash()

    #Layout setup
    app.layout = html.Div(children=[
        html.H1(children = "Dashboard test"),
        dcc.Dropdown(id="dataset",
                    options = [{'label': file[20:-5], 'value' : file}
                                for file in file_list],
                    value = file_list[0]),
        dcc.Graph(id = "graphs")
    ])

    #Callback function
    @app.callback(
        Output(component_id = "graphs", component_property="figure"),
        Input(component_id = "dataset", component_property = "value")
    )

    def update_graphs(selected_dataset):
        #Load dataset
        f = open(selected_dataset, "r", encoding="utf-8")
        data = json.loads(f.read())
        f.close()
        
        #Generate graphs
        fig_frequent_keywords = frequent_keywords_hist(data)
        fig_country_hist, fig_country_map = mentionned_countries_map(data)
        
        # Create a subplot
        
        fig = make_subplots(
            rows=2, cols=2,
            #subplot_titles=("Frequent Keywords", "Country Histogram", "Country Map"),
            specs=[
                [{"type": "xy", "colspan": 1}, {"type": "xy", "colspan": 1}],  # Row 1: cartesian plots
                [{"type": "geo", "colspan": 2}, None]  # Row 2: map (geo) and empty cell
            ],
            column_widths=[0.4, 0.4]  # Adjust column widths
        )

        # Add traces from fig_frequent_keywords
        for trace in fig_frequent_keywords.data:
            fig.add_trace(trace, row=1, col=1)

        # Add traces from fig_country_hist
        for trace in fig_country_hist.data:
            fig.add_trace(trace, row=1, col=2)

        # Add traces from fig_country_map
        for trace in fig_country_map.data:
            fig.add_trace(trace, row=2, col=1)

        # Update layout for the subplot
        fig.update_layout(
            height=1000,  # Adjust height to fit the content
            width = 1600,
            showlegend=False
        )
        
        return fig
    return app
